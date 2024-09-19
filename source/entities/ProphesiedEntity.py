class ProphesiedEntity:
    def __init__(
        self,
        id,
        stock_id,
        date,
        trend,
        yhat_lower,
        yhat_upper,
        trend_lower,
        trend_upper,
        additive_terms,
        additive_terms_lower,
        additive_terms_upper,
        weekly,
        weekly_lower,
        weekly_upper,
        multiplicative_terms,
        multiplicative_terms_lower,
        multiplicative_terms_upper,
        yhat
    ):
        self.id = id
        self.stock_id = stock_id
        self.date = date
        self.trend = trend
        self.yhat_lower = yhat_lower
        self.yhat_upper = yhat_upper
        self.trend_lower = trend_lower
        self.trend_upper = trend_upper
        self.additive_terms = additive_terms
        self.additive_terms_lower = additive_terms_lower
        self.additive_terms_upper = additive_terms_upper
        self.weekly = weekly
        self.weekly_lower = weekly_lower
        self.weekly_upper = weekly_upper
        self.multiplicative_terms = multiplicative_terms
        self.multiplicative_terms_lower = multiplicative_terms_lower
        self.multiplicative_terms_upper = multiplicative_terms_upper
        self.yhat = yhat