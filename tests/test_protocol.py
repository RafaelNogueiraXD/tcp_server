import pytest
from tcp_server.protocol import Protocol, Response

def test_ping_command():
    protocol = Protocol()
    response = protocol.handle_command("PING")
    assert response.status == "OK"
    assert response.message == "PONG"

def test_echo_command():
    protocol = Protocol()
    message = "Hello World"
    response = protocol.handle_command("ECHO", message)
    assert response.status == "OK"
    assert response.message == message

def test_time_command():
    protocol = Protocol()
    response = protocol.handle_command("TIME")
    assert response.status == "OK"
    assert "Current time is" in response.message

def test_info_command():
    protocol = Protocol()
    response = protocol.handle_command("INFO")
    assert response.status == "OK"
    assert response.data is not None
    assert "name" in response.data
    assert "version" in response.data

def test_unknown_command():
    protocol = Protocol()
    response = protocol.handle_command("UNKNOWN")
    assert response.status == "ERROR"
    assert response.message == "Unknown command"
