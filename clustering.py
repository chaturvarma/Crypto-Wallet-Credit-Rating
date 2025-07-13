from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def cluster_and_rank(df, n_clusters=6):
    selected_features = [
        'repayment_ratio',
        'withdraw_ratio',
        'total_deposit_usd',
        'net_borrowed_usd',
        'num_total_txns',
        'last_active_days_ago',
        'dominant_asset_ratio'
    ]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[selected_features])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    df['cluster'] = kmeans.fit_predict(X_scaled)

    cluster_means = df.groupby('cluster')[['repayment_ratio', 'total_deposit_usd']].mean()
    cluster_means['score_basis'] = (
        0.6 * cluster_means['repayment_ratio'] +
        0.4 * cluster_means['total_deposit_usd'].rank() / cluster_means['total_deposit_usd'].rank().max()
    )
    ranked_clusters = cluster_means['score_basis'].sort_values(ascending=False).index

    target_scores = [100, 80, 60, 40, 20, 0][:n_clusters]
    cluster_to_score = {cluster: target_scores[i] for i, cluster in enumerate(ranked_clusters)}

    df['credit_score'] = df['cluster'].map(cluster_to_score)
    
    return df