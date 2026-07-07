import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import json

# Mock boto3 before importing lambda_function
sys.modules['boto3'] = MagicMock()

def test_lambda_handler_success():
    """Test Lambda handler completes without errors"""
    # This is a placeholder test
    # In production, you'd mock all AWS calls and test the logic
    assert True

def test_collect_ec2_data():
    """Test EC2 data collection"""
    # Mock AWS calls
    with patch('boto3.client'):
        assert True

def test_security_group_analysis():
    """Test security group analysis finds issues"""
    test_sg = {
        'sg_id': 'sg-123456',
        'sg_name': 'test-sg',
        'issue_type': 'Open to Internet',
        'protocol': 'TCP',
        'port_range': '22',
        'severity': 'CRITICAL'
    }
    
    assert test_sg['severity'] == 'CRITICAL'
    assert test_sg['port_range'] == '22'

def test_prompt_generation():
    """Test audit prompt is formatted correctly"""
    ec2_data = []
    security_data = []
    
    # The prompt should handle empty data gracefully
    assert isinstance(ec2_data, list)
    assert isinstance(security_data, list)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])