"""
Comprehensive tests for TradePlanner and TradeManager.
Tests position sizing, risk management, and trade execution flows.
"""

import pytest
import pandas as pd
from datetime import datetime

from market.historical import HistoricalService
from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator
from indicators.atr import ATRIndicator
from indicators.volume import VolumeIndicator
from ai.decision_engine import DecisionEngine
from ai.trade_planner import TradePlanner, TradeManager, TradePlan
from core.enums import Recommendation


class TestTradePlanCreation:
    """Test TradePlan dataclass creation and conversions."""
    
    def test_trade_plan_creation(self):
        """Test creating a TradePlan dataclass."""
        plan = TradePlan(
            symbol="RELIANCE",
            recommendation=Recommendation.BUY.value,
            entry_price=2000.0,
            stop_loss=1950.0,
            target1=2050.0,
            target2=2100.0,
            position_size=100,
            risk_amount=50.0,
            reward_amount=100.0,
            risk_reward_ratio=2.0,
            confidence=85.0,
        )
        
        assert plan.symbol == "RELIANCE"
        assert plan.recommendation == Recommendation.BUY.value
        assert plan.entry_price == 2000.0
        assert plan.stop_loss == 1950.0
        assert plan.position_size == 100
        assert plan.confidence == 85.0
        print("✓ TradePlan creation test passed")
    
    def test_trade_plan_to_signal(self):
        """Test converting TradePlan to Signal."""
        plan = TradePlan(
            symbol="TCS",
            recommendation=Recommendation.SELL.value,
            entry_price=3500.0,
            stop_loss=3550.0,
            target1=3400.0,
            target2=3300.0,
            position_size=50,
            risk_amount=50.0,
            reward_amount=100.0,
            risk_reward_ratio=2.0,
            confidence=75.0,
        )
        
        signal = plan.to_signal()
        
        assert signal.symbol == "TCS"
        assert signal.recommendation == Recommendation.SELL.value
        assert signal.stop_loss == 3550.0
        assert signal.target == 3400.0
        print("✓ TradePlan to Signal conversion test passed")


class TestTradePlannerValidation:
    """Test TradePlanner input validation."""
    
    def test_validate_hold_signal(self):
        """Test that HOLD signal raises error."""
        history = HistoricalService()
        df = history.load("INFY")
        
        df = EMAIndicator.calculate(df)
        df = RSIIndicator.calculate(df)
        df = MACDIndicator.calculate(df)
        df = ATRIndicator.calculate(df)
        df = VolumeIndicator.calculate(df)
        
        # Modify dataframe to force HOLD signal
        df.loc[df.index[-1], 'RSI'] = 50
        df.loc[df.index[-1], 'EMA_20'] = df.loc[df.index[-1], 'EMA_50']
        
        decision = DecisionEngine.analyze(df, symbol="INFY")
        
        if decision.signal == Recommendation.HOLD.value:
            with pytest.raises(ValueError, match="Cannot plan trade for HOLD signal"):
                TradePlanner.plan(decision)
            print("✓ HOLD signal validation test passed")
    
    def test_validate_invalid_entry_price(self):
        """Test validation of invalid entry price."""
        from core.models import DecisionOutput
        
        decision = DecisionOutput(
            symbol="TEST",
            signal=Recommendation.BUY.value,
            confidence=80,
            entry=-100.0,  # Invalid
            stop_loss=90.0,
            target1=120.0,
            target2=150.0,
            risk_reward_ratio=2.0,
        )
        
        with pytest.raises(ValueError, match="Invalid entry price"):
            TradePlanner.plan(decision)
        print("✓ Invalid entry price validation test passed")
    
    def test_validate_buy_stop_loss_above_entry(self):
        """Test BUY signal with stop loss above entry."""
        from core.models import DecisionOutput
        
        decision = DecisionOutput(
            symbol="TEST",
            signal=Recommendation.BUY.value,
            confidence=80,
            entry=100.0,
            stop_loss=110.0,  # Above entry (invalid for BUY)
            target1=120.0,
            target2=150.0,
            risk_reward_ratio=2.0,
        )
        
        with pytest.raises(ValueError, match="Stop loss must be below entry"):
            TradePlanner.plan(decision)
        print("✓ BUY stop loss validation test passed")


class TestPositionSizing:
    """Test position sizing calculations."""
    
    def test_position_size_calculation(self):
        """Test position size based on risk management."""
        from core.models import DecisionOutput
        
        decision = DecisionOutput(
            symbol="RELIANCE",
            signal=Recommendation.BUY.value,
            confidence=85,
            entry=2000.0,
            stop_loss=1950.0,
            target1=2050.0,
            target2=2100.0,
            risk_reward_ratio=2.0,
        )
        
        account_size = 100000
        risk_percent = 2.0  # Risk 2% per trade
        
        position_size = TradePlanner._calculate_position_size(
            decision, account_size, risk_percent
        )
        
        # Risk amount = 100000 * 2% = 2000
        # Price diff = 2000 - 1950 = 50
        # Position size = 2000 / 50 = 40
        assert position_size == 40.0
        print(f"✓ Position size calculation test passed: {position_size} units")
    
    def test_position_size_with_different_account(self):
        """Test position size scales with account size."""
        from core.models import DecisionOutput
        
        decision = DecisionOutput(
            symbol="INFY",
            signal=Recommendation.BUY.value,
            confidence=80,
            entry=1500.0,
            stop_loss=1450.0,
            target1=1550.0,
            target2=1600.0,
            risk_reward_ratio=2.0,
        )
        
        # Test with small account
        pos_small = TradePlanner._calculate_position_size(decision, 10000, 1.0)
        
        # Test with large account
        pos_large = TradePlanner._calculate_position_size(decision, 1000000, 1.0)
        
        # Larger account should have larger position
        assert pos_large > pos_small
        print(f"✓ Position scaling test passed: {pos_small} → {pos_large} units")


class TestRiskRewardCalculation:
    """Test risk-reward calculations."""
    
    def test_risk_reward_ratio_buy(self):
        """Test RR ratio calculation for BUY."""
        from core.models import DecisionOutput
        
        decision = DecisionOutput(
            symbol="RELIANCE",
            signal=Recommendation.BUY.value,
            confidence=85,
            entry=2000.0,
            stop_loss=1950.0,
            target1=2050.0,
            target2=2100.0,
            risk_reward_ratio=2.0,
        )
        
        risk, reward, rr = TradePlanner._calculate_risk_reward(decision)
        
        # Risk = 2000 - 1950 = 50
        # Reward = 2050 - 2000 = 50
        # RR = 50 / 50 = 1.0
        assert risk == 50.0
        assert reward == 50.0
        assert rr == 1.0
        print(f"✓ Risk-Reward ratio test passed: 1:{rr}")
    
    def test_risk_reward_ratio_sell(self):
        """Test RR ratio calculation for SELL."""
        from core.models import DecisionOutput
        
        decision = DecisionOutput(
            symbol="TCS",
            signal=Recommendation.SELL.value,
            confidence=80,
            entry=3500.0,
            stop_loss=3600.0,
            target1=3400.0,
            target2=3300.0,
            risk_reward_ratio=2.0,
        )
        
        risk, reward, rr = TradePlanner._calculate_risk_reward(decision)
        
        # Risk = 3600 - 3500 = 100
        # Reward = 3500 - 3400 = 100
        # RR = 100 / 100 = 1.0
        assert risk == 100.0
        assert reward == 100.0
        assert rr == 1.0
        print(f"✓ SELL Risk-Reward ratio test passed: 1:{rr}")


class TestTradePlannerIntegration:
    """Integration tests for TradePlanner with DecisionEngine."""
    
    def test_plan_from_decision_engine(self):
        """Test creating trade plan from DecisionEngine output."""
        history = HistoricalService()
        df = history.load("RELIANCE")
        
        df = EMAIndicator.calculate(df)
        df = RSIIndicator.calculate(df)
        df = MACDIndicator.calculate(df)
        df = ATRIndicator.calculate(df)
        df = VolumeIndicator.calculate(df)
        
        decision = DecisionEngine.analyze(df, symbol="RELIANCE")
        print(f"Decision: {decision.signal} (confidence: {decision.confidence:.1f}%)")
        
        # Only plan if not HOLD
        if decision.signal != Recommendation.HOLD.value:
            plan = TradePlanner.plan(decision, account_size=100000)
            
            assert plan.symbol == "RELIANCE"
            assert plan.entry_price == decision.entry
            assert plan.stop_loss == decision.stop_loss
            assert plan.confidence == decision.confidence
            assert plan.position_size > 0
            print(f"✓ Trade plan created: {plan.position_size:.2f} units @ ₹{plan.entry_price:.2f}")
    
    def test_plan_batch(self):
        """Test batch planning for multiple symbols."""
        symbols = ["RELIANCE", "TCS", "INFY"]
        decisions = []
        
        history = HistoricalService()
        
        for symbol in symbols:
            try:
                df = history.load(symbol)
                df = EMAIndicator.calculate(df)
                df = RSIIndicator.calculate(df)
                df = MACDIndicator.calculate(df)
                df = ATRIndicator.calculate(df)
                df = VolumeIndicator.calculate(df)
                
                decision = DecisionEngine.analyze(df, symbol=symbol)
                decisions.append(decision)
            except Exception as e:
                print(f"⚠️  Skipped {symbol}: {e}")
        
        # Create batch plans
        plans = TradePlanner.plan_batch(decisions, account_size=300000)
        
        assert len(plans) > 0
        print(f"✓ Batch planning created {len(plans)} trade plans")


class TestTradeManager:
    """Test TradeManager for real-time trade monitoring."""
    
    def test_manager_add_plan(self):
        """Test adding plans to manager."""
        manager = TradeManager()
        
        plan = TradePlan(
            symbol="RELIANCE",
            recommendation=Recommendation.BUY.value,
            entry_price=2000.0,
            stop_loss=1950.0,
            target1=2050.0,
            target2=2100.0,
            position_size=100,
            risk_amount=50.0,
            reward_amount=100.0,
            risk_reward_ratio=2.0,
            confidence=85.0,
        )
        
        manager.add_plan(plan)
        
        assert "RELIANCE" in manager.active_plans
        assert len(manager.get_active_plans()) == 1
        print("✓ Manager add plan test passed")
    
    def test_manager_buy_stop_loss_trigger(self):
        """Test stop loss trigger for BUY trade."""
        manager = TradeManager()
        
        plan = TradePlan(
            symbol="RELIANCE",
            recommendation=Recommendation.BUY.value,
            entry_price=2000.0,
            stop_loss=1950.0,
            target1=2050.0,
            target2=2100.0,
            position_size=100,
            risk_amount=50.0,
            reward_amount=100.0,
            risk_reward_ratio=2.0,
            confidence=85.0,
        )
        
        manager.add_plan(plan)
        
        # Update with price below stop loss
        action = manager.update_with_price("RELIANCE", 1940.0)
        
        assert action == "EXIT_STOP_LOSS"
        assert "RELIANCE" not in manager.active_plans
        assert len(manager.completed_plans) == 1
        print("✓ Buy stop loss trigger test passed")
    
    def test_manager_buy_target_trigger(self):
        """Test target trigger for BUY trade."""
        manager = TradeManager()
        
        plan = TradePlan(
            symbol="TCS",
            recommendation=Recommendation.BUY.value,
            entry_price=3000.0,
            stop_loss=2950.0,
            target1=3050.0,
            target2=3100.0,
            position_size=50,
            risk_amount=50.0,
            reward_amount=50.0,
            risk_reward_ratio=1.0,
            confidence=80.0,
            take_partial_at_target1=False,
        )
        
        manager.add_plan(plan)
        
        # Update with price at target1
        action = manager.update_with_price("TCS", 3050.0)
        
        assert action == "EXIT_TARGET1"
        assert "TCS" not in manager.active_plans
        print("✓ Buy target trigger test passed")
    
    def test_manager_sell_stop_loss_trigger(self):
        """Test stop loss trigger for SELL trade."""
        manager = TradeManager()
        
        plan = TradePlan(
            symbol="INFY",
            recommendation=Recommendation.SELL.value,
            entry_price=1500.0,
            stop_loss=1550.0,  # Above entry for SELL
            target1=1450.0,
            target2=1400.0,
            position_size=75,
            risk_amount=50.0,
            reward_amount=50.0,
            risk_reward_ratio=1.0,
            confidence=80.0,
        )
        
        manager.add_plan(plan)
        
        # Update with price above stop loss
        action = manager.update_with_price("INFY", 1560.0)
        
        assert action == "EXIT_STOP_LOSS"
        assert "INFY" not in manager.active_plans
        print("✓ Sell stop loss trigger test passed")
    
    def test_manager_get_plan_status(self):
        """Test getting plan status."""
        manager = TradeManager()
        
        plan = TradePlan(
            symbol="RELIANCE",
            recommendation=Recommendation.BUY.value,
            entry_price=2000.0,
            stop_loss=1950.0,
            target1=2050.0,
            target2=2100.0,
            position_size=100,
            risk_amount=50.0,
            reward_amount=100.0,
            risk_reward_ratio=2.0,
            confidence=85.0,
        )
        
        manager.add_plan(plan)
        status = manager.get_plan_status("RELIANCE")
        
        assert status is not None
        assert status["symbol"] == "RELIANCE"
        assert status["entry"] == 2000.0
        assert status["risk_reward"] == 2.0
        print("✓ Get plan status test passed")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TRADE PLANNER TEST SUITE")
    print("="*70)
    
    # Run test classes
    test_creation = TestTradePlanCreation()
    test_creation.test_trade_plan_creation()
    test_creation.test_trade_plan_to_signal()
    
    test_validation = TestTradePlannerValidation()
    test_validation.test_validate_invalid_entry_price()
    test_validation.test_validate_buy_stop_loss_above_entry()
    
    test_sizing = TestPositionSizing()
    test_sizing.test_position_size_calculation()
    test_sizing.test_position_size_with_different_account()
    
    test_rr = TestRiskRewardCalculation()
    test_rr.test_risk_reward_ratio_buy()
    test_rr.test_risk_reward_ratio_sell()
    
    test_integration = TestTradePlannerIntegration()
    test_integration.test_plan_from_decision_engine()
    test_integration.test_plan_batch()
    
    test_manager = TestTradeManager()
    test_manager.test_manager_add_plan()
    test_manager.test_manager_buy_stop_loss_trigger()
    test_manager.test_manager_buy_target_trigger()
    test_manager.test_manager_sell_stop_loss_trigger()
    test_manager.test_manager_get_plan_status()
    
    print("\n" + "="*70)
    print("✅ ALL TRADE PLANNER TESTS PASSED")
    print("="*70)
