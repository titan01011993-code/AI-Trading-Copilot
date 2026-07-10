"""
TradePlanner - Converts trading decisions into executable trade plans.

Transforms DecisionOutput from DecisionEngine into comprehensive trade plans
with detailed entry, exit, sizing, and management rules.
"""

from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime

from core.models import DecisionOutput, Signal
from core.enums import Recommendation


@dataclass(slots=True)
class TradePlan:
    """
    Complete trade plan with entry, exits, and management rules.
    """
    symbol: str
    recommendation: str  # BUY, SELL, HOLD
    entry_price: float
    stop_loss: float
    target1: float
    target2: float
    position_size: float
    risk_amount: float
    reward_amount: float
    risk_reward_ratio: float
    confidence: float
    
    # Management rules
    trail_stop_at_target1: bool = True
    move_stop_to_entry_at_target1: bool = False
    take_partial_at_target1: bool = True
    partial_size_at_target1: float = 0.5  # 50% of position
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    decision_output: Optional[DecisionOutput] = None
    analysis_reasons: List[str] = field(default_factory=list)
    
    def to_signal(self) -> Signal:
        """Convert TradePlan to Signal dataclass."""
        return Signal(
            symbol=self.symbol,
            trend="",  # To be filled by caller
            recommendation=self.recommendation,
            score=self.confidence,
            confidence=self.confidence,
            stop_loss=self.stop_loss,
            target=self.target1,
        )


class TradePlanner:
    """
    Production-grade trade planner that converts DecisionEngine output
    into actionable trade plans with risk management rules.
    
    Features:
    - Position sizing based on risk
    - Multi-level take profits
    - Stop loss placement
    - Risk-reward validation
    - Management rules (trailing stops, partial takes)
    """
    
    # Configuration
    DEFAULT_POSITION_SIZE = 1.0  # In units (e.g., shares/contracts)
    DEFAULT_RISK_PERCENT = 1.0   # 1% of account per trade
    MIN_RISK_REWARD = 1.0        # Minimum acceptable RR ratio
    
    @staticmethod
    def _validate_decision(decision: DecisionOutput) -> None:
        """
        Validate DecisionOutput before planning.
        
        Args:
            decision: DecisionOutput from DecisionEngine
            
        Raises:
            ValueError: If decision is invalid
        """
        if decision.signal == Recommendation.HOLD.value:
            raise ValueError("Cannot plan trade for HOLD signal")
        
        if decision.entry <= 0:
            raise ValueError(f"Invalid entry price: {decision.entry}")
        
        if decision.stop_loss <= 0:
            raise ValueError(f"Invalid stop loss: {decision.stop_loss}")
        
        if decision.signal == Recommendation.BUY.value:
            if decision.stop_loss >= decision.entry:
                raise ValueError("Stop loss must be below entry for BUY")
            if decision.target1 <= decision.entry:
                raise ValueError("Target1 must be above entry for BUY")
        
        if decision.risk_reward_ratio < TradePlanner.MIN_RISK_REWARD:
            raise ValueError(
                f"Risk-reward ratio {decision.risk_reward_ratio:.2f} "
                f"below minimum {TradePlanner.MIN_RISK_REWARD:.2f}"
            )
    
    @staticmethod
    def _calculate_position_size(
        decision: DecisionOutput,
        account_size: float,
        risk_percent: float = DEFAULT_RISK_PERCENT,
    ) -> float:
        """
        Calculate position size based on risk management.
        
        Args:
            decision: DecisionOutput from DecisionEngine
            account_size: Total trading account size
            risk_percent: Percentage of account to risk per trade
            
        Returns:
            Position size in units
        """
        # Calculate risk amount
        risk_amount = account_size * (risk_percent / 100)
        
        # Calculate distance to stop loss
        price_diff = abs(decision.entry - decision.stop_loss)
        
        if price_diff == 0:
            return 0.0
        
        # Position size = risk amount / price difference
        position_size = risk_amount / price_diff
        
        return max(0.0, position_size)
    
    @staticmethod
    def _calculate_risk_reward(decision: DecisionOutput) -> tuple:
        """
        Calculate risk amount, reward amount, and ratio.
        
        Args:
            decision: DecisionOutput from DecisionEngine
            
        Returns:
            Tuple of (risk_amount, reward_amount, rr_ratio)
        """
        risk = abs(decision.entry - decision.stop_loss)
        reward = abs(decision.target1 - decision.entry)
        
        if risk == 0:
            return 0.0, 0.0, 0.0
        
        rr_ratio = reward / risk if risk > 0 else 0.0
        return round(risk, 2), round(reward, 2), round(rr_ratio, 2)
    
    @staticmethod
    def plan(
        decision: DecisionOutput,
        account_size: float = 100000,
        risk_percent: float = DEFAULT_RISK_PERCENT,
    ) -> TradePlan:
        """
        Create a complete trade plan from DecisionEngine output.
        
        Args:
            decision: DecisionOutput from DecisionEngine
            account_size: Total trading account size (default: ₹100,000)
            risk_percent: Percentage of account to risk per trade
            
        Returns:
            TradePlan ready for execution
            
        Raises:
            ValueError: If decision is invalid for planning
        """
        # Validate decision
        TradePlanner._validate_decision(decision)
        
        # Calculate position size
        position_size = TradePlanner._calculate_position_size(
            decision, account_size, risk_percent
        )
        
        # Calculate risk and reward
        risk_amount, reward_amount, rr_ratio = TradePlanner._calculate_risk_reward(decision)
        
        # Create trade plan
        plan = TradePlan(
            symbol=decision.symbol,
            recommendation=decision.signal,
            entry_price=decision.entry,
            stop_loss=decision.stop_loss,
            target1=decision.target1,
            target2=decision.target2,
            position_size=position_size,
            risk_amount=risk_amount,
            reward_amount=reward_amount,
            risk_reward_ratio=rr_ratio,
            confidence=decision.confidence,
            decision_output=decision,
            analysis_reasons=decision.reasons,
        )
        
        return plan
    
    @staticmethod
    def plan_batch(
        decisions: List[DecisionOutput],
        account_size: float = 100000,
        risk_percent: float = DEFAULT_RISK_PERCENT,
    ) -> List[TradePlan]:
        """
        Create trade plans for multiple decisions.
        
        Args:
            decisions: List of DecisionOutput objects
            account_size: Total trading account size
            risk_percent: Percentage of account to risk per trade
            
        Returns:
            List of TradePlan objects
        """
        plans = []
        
        for decision in decisions:
            try:
                plan = TradePlanner.plan(decision, account_size, risk_percent)
                plans.append(plan)
            except ValueError as e:
                print(f"⚠️  Skipped {decision.symbol}: {e}")
                continue
        
        return plans


class TradeManager:
    """
    Manages active trade plans with real-time updates and execution signals.
    """
    
    def __init__(self):
        """Initialize trade manager."""
        self.active_plans: dict = {}
        self.completed_plans: list = []
    
    def add_plan(self, plan: TradePlan) -> None:
        """Add a trade plan to active plans."""
        self.active_plans[plan.symbol] = plan
    
    def update_with_price(
        self,
        symbol: str,
        current_price: float,
    ) -> Optional[str]:
        """
        Update plan with current price and return action if needed.
        
        Args:
            symbol: Stock symbol
            current_price: Current market price
            
        Returns:
            Action string if triggered (e.g., "EXIT_TARGET1", "EXIT_STOP_LOSS", None)
        """
        if symbol not in self.active_plans:
            return None
        
        plan = self.active_plans[symbol]
        
        # For BUY trades
        if plan.recommendation == Recommendation.BUY.value:
            # Check stop loss
            if current_price <= plan.stop_loss:
                self.active_plans.pop(symbol)
                self.completed_plans.append(plan)
                return "EXIT_STOP_LOSS"
            
            # Check target1
            if current_price >= plan.target1:
                if plan.take_partial_at_target1:
                    # Partial exit, keep rest
                    return "EXIT_PARTIAL_TARGET1"
                else:
                    # Full exit
                    self.active_plans.pop(symbol)
                    self.completed_plans.append(plan)
                    return "EXIT_TARGET1"
            
            # Check target2
            if current_price >= plan.target2:
                self.active_plans.pop(symbol)
                self.completed_plans.append(plan)
                return "EXIT_TARGET2"
        
        # For SELL trades
        elif plan.recommendation == Recommendation.SELL.value:
            # Check stop loss (above entry for short)
            if current_price >= plan.stop_loss:
                self.active_plans.pop(symbol)
                self.completed_plans.append(plan)
                return "EXIT_STOP_LOSS"
            
            # Check target1 (below entry for short)
            if current_price <= plan.target1:
                if plan.take_partial_at_target1:
                    return "EXIT_PARTIAL_TARGET1"
                else:
                    self.active_plans.pop(symbol)
                    self.completed_plans.append(plan)
                    return "EXIT_TARGET1"
            
            # Check target2
            if current_price <= plan.target2:
                self.active_plans.pop(symbol)
                self.completed_plans.append(plan)
                return "EXIT_TARGET2"
        
        return None
    
    def get_active_plans(self) -> List[TradePlan]:
        """Get all active trade plans."""
        return list(self.active_plans.values())
    
    def get_plan_status(self, symbol: str) -> Optional[dict]:
        """Get detailed status of a plan."""
        if symbol not in self.active_plans:
            return None
        
        plan = self.active_plans[symbol]
        
        return {
            "symbol": plan.symbol,
            "recommendation": plan.recommendation,
            "entry": plan.entry_price,
            "stop_loss": plan.stop_loss,
            "target1": plan.target1,
            "target2": plan.target2,
            "position_size": plan.position_size,
            "risk_reward": plan.risk_reward_ratio,
            "confidence": plan.confidence,
        }
