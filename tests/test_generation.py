from httpx import ConnectError
import ollama
import pytest


def test_ollamaserver():
    """Check if the ollama server is running or not. If the code does not return a connect error, it passes the test."""
    try:
        ollama.list()["models"]
    except Exception as e:
        assert e == ConnectError


def test_checkinstalledmodels():
    """Check if at least one model is installed with ollama."""
    try:
        INSTALLEDMODELS: list[str] = []
        for modelName in ollama.list()["models"]:
            # print(modelName["name"])
            INSTALLEDMODELS.append(modelName["name"])
        assert len(INSTALLEDMODELS) > 0
    except ConnectError:
        raise Exception(
            "The ollama server is not online. \nUse ollama serve to run the ollama daemon."
        )
