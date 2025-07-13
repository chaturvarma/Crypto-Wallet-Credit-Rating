# Crypto Wallet Credit Rating

## Project Overview

This project aims to score crypto wallets based on their on-chain activity and credit behavior using transaction data from the Compound V2 protocol. By applying data extraction, feature engineering, and clustering techniques, we assign each wallet a credit score ranging from 0 to 100, which can serve as a proxy for trustworthiness and financial behavior in decentralized finance (DeFi)

## Dataset

The dataset consists of Compound V2 transaction logs in JSON format. Each record corresponds to a wallet interacting with the protocol through actions such as deposit, borrow, repay, withdraw, and liquidation

## 🔧 Data Extraction

Python function (`extract_data`) was used to extract the following fields from each JSON:
- `account_id`: Wallet address
- `amount_usd`: USD value of transaction
- `asset_symbol`: Token involved
- `timestamp`: UNIX timestamp
- `transaction_type`: Coded as:
  - `0`: Deposit
  - `1`: Withdraw
  - `2`: Borrow
  - `3`: Repay
  - `4`: Liquidate

## 🧠 Feature Engineering

From the raw transaction logs, several wallet-level features were engineered that reflect financial behavior:

| Feature | Description |
|--------|-------------|
| `num_total_txns` | Total number of transactions |
| `num_deposits`, `num_borrows`, ... | Action-type specific counts |
| `total_deposit_usd`, `total_repay_usd`, etc. | Total value in USD for each action |
| `repayment_ratio` | `total_repaid / total_borrowed` |
| `withdraw_ratio` | `total_withdrawn / total_deposited` |
| `net_borrowed_usd` | `total_borrowed - total_repaid` |
| `active_days_span` | Number of days between first and last activity |
| `last_active_days_ago` | How recently the wallet was active |
| `unique_assets_used` | Number of distinct tokens used |
| `dominant_asset_ratio` | Share of most used token in transactions |
| `has_borrow_no_repay` | Wallet borrowed but never repaid (flag) |
| `has_withdraw_no_deposit` | Wallet withdrew without depositing (flag) |

### Clustering

Instead of using a hand-crafted score metric directly, we apply KMeans clustering on selected key behavioral features:

- `repayment_ratio`
- `withdraw_ratio`
- `total_deposit_usd`
- `net_borrowed_usd`
- `num_total_txns`
- `last_active_days_ago`
- `dominant_asset_ratio`

Each cluster is evaluated using the following custom metric:

```python
score_basis = 0.6 * repayment_ratio + 0.4 * (ranked total_deposit_usd)
```

Clusters are sorted by average `score_basis`, and mapped to scores:

```
Cluster Rank → Credit Score
Best         → 100  
Next         → 80  
...          → 0