# Binance Futures Testnet Trading Bot

A Python-based Command Line Interface (CLI) application designed to place and manage trades on the Binance Futures Testnet (USDT-M). 

This project was built to demonstrate secure REST API communication using HMAC SHA256 encryption, modular architecture, and robust error handling.

## 🚀 Features
* **Order Placement:** Supports both `MARKET` and `LIMIT` order types for `BUY` and `SELL` sides.
* **Secure Authentication:** Implements direct Binance API payload signing (HMAC SHA256) without relying on heavy third-party wrappers.
* **Validation Layer:** Sanitizes and validates user inputs before communicating with the exchange.
* **Comprehensive Logging:** Records all API requests, responses, and errors to both the console and a local `.log` file.

---

## 📂 Project Structure
```text
trading_bot/
├── logs/
│   └── trading_bot.log    # Auto-generated execution logs
├── .env                   # Environment variables (API Keys - Not uploaded)
├── cli.py                 # Main application code and CLI entry point
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
