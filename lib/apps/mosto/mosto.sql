CREATE TABLE IF NOT EXISTS fct_momemtum_stock_daily(
    ds varchar,
    momemtum_stock varchar,
    revenue_one_yr_ago float,
    revenue_two_yr_ago float,
    price_today float,
    price_50day_moving_avg float,
    price_200day_moving_avg float
);


CREATE TABLE IF NOT EXISTS dim_momemtum_stocks_i_own(
    momemtum_stock varchar,
    purchase_price float,
    ds_purchased varchar
);
