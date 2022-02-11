from django.urls import path
from lastestPrice import views

urlpatterns = [
    # 获取最新价格 （新浪财经）
    path('getLastPrice/<ticker>', views.getLastestPrice),
    # 获取最新价格 （天勤版）
    path('getTQLastPrice/<ticker>', views.getTQLastPrice),
    # 动态数据同步
    # path('getAllDynamicData/', views.getAllDynamicDate),
    # 期货套利组合动静态表更新
    path('getAllFuturePortfolio/', views.getAllFuturePortfolio),

    # 期货收盘价和结算价
    path('getTQCloseAndSettle/<ticker>', views.getTQCloseAndSettle),

    # 从保证金率表格获取不同类型保证金率 (future_latest_contract_settle) 默认参数 可以省略trade_date参数 默认当天
    path('getMarginRate/<ticker>/<buy_or_sell>/<hedge_or_speculate>/', views.getMarginRate),
    # 从保证金率表格获取不同类型保证金率 (future_latest_contract_settle) 完整路径 可以指定trade_date
    # path('getMarginRate/<ticker>/<buy_or_sell>/<hedge_or_speculate>/<str:trade_date>/', views.getMarginRate),
]