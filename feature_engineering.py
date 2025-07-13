import pandas as pd

def feature_engineering(df):
    df['timestamp'] = pd.to_datetime(pd.to_numeric(df['timestamp'], errors='coerce'), unit='s')

    grouped = df.groupby('account_id')

    feature_rows = []

    for account_id, group in grouped:
        features = {"wallet": account_id}

        group_sorted = group.sort_values(by='timestamp')
        timestamps = group_sorted['timestamp']

        features['num_total_txns'] = len(group)
        features['num_days_active'] = group['timestamp'].dt.date.nunique()
        features['active_days_span'] = (timestamps.max() - timestamps.min()).days + 1
        features['last_active_days_ago'] = (pd.Timestamp.now() - timestamps.max()).days
        features['avg_txns_per_day'] = features['num_total_txns'] / features['active_days_span'] if features['active_days_span'] > 0 else 0

        tx_types = {
            0: 'deposit',
            1: 'withdraw',
            2: 'borrow',
            3: 'repay',
            4: 'liquidate'
        }

        for code, name in tx_types.items():
            sub = group[group['transaction_type'] == code]
            features[f'num_{name}s'] = len(sub)
            features[f'total_{name}_usd'] = sub['amount_usd'].sum()

        total_borrowed = features['total_borrow_usd']
        total_repaid = features['total_repay_usd']
        total_deposited = features['total_deposit_usd']
        total_withdrawn = features['total_withdraw_usd']

        features['repayment_ratio'] = total_repaid / total_borrowed if total_borrowed > 0 else 0
        features['withdraw_ratio'] = total_withdrawn / total_deposited if total_deposited > 0 else 0
        features['net_borrowed_usd'] = total_borrowed - total_repaid

        features['unique_assets_used'] = group['asset_symbol'].nunique()
        asset_counts = group['asset_symbol'].value_counts(normalize=True)
        features['dominant_asset_ratio'] = asset_counts.iloc[0] if not asset_counts.empty else 0

        features['has_borrow_no_repay'] = int((total_borrowed > 0) and (total_repaid == 0))
        features['has_withdraw_no_deposit'] = int((total_withdrawn > 0) and (total_deposited == 0))

        feature_rows.append(features)

    return pd.DataFrame(feature_rows)