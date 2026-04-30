// 初始化 ECharts 实例
var chartDom = document.getElementById('graph-container');
var myChart = echarts.init(chartDom);

// 模拟从后端获取的团伙节点数据
// 在实际演示时，你可以通过 fetch("http://127.0.0.1:8000/api/v1/predict") 获取真实数据
var option = {
    title: { text: '智鉴·网盾 - 实时黑产团伙关系图谱', textStyle: {color: '#fff'} },
    series: [{
        type: 'graph',
        layout: 'force',
        symbolSize: 40,
        roam: true,
        label: { show: true },
        edgeSymbol: ['circle', 'arrow'],
        data: [
            { name: '交易_52', category: 1, itemStyle: {color: '#ff4d4f'}, value: '高危团伙核心' },
            { name: '用户_A', category: 0, itemStyle: {color: '#73d13d'} },
            { name: '用户_B', category: 0, itemStyle: {color: '#73d13d'} }
        ],
        links: [
            { source: '交易_52', target: '用户_A', label: {show: true, formatter: '共享IP'} },
            { source: '交易_52', target: '用户_B', label: {show: true, formatter: '相同地址'} }
        ],
        force: { repulsion: 1000 }
    }]
};

myChart.setOption(option);

// 监听点击事件，点击红点时调用后端 Qwen 报告
myChart.on('click', function (params) {
    if (params.data.itemStyle.color === '#ff4d4f') {
        document.getElementById('loading').style.display = 'block';
        // 模拟调用你的 FastAPI 接口
        fetch("http://127.0.0.1:8000/api/v1/predict", {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                transaction_id: "TX_52",
                amount: 8848.0,
                hour: 3,
                card_id: "CARD_001",
                address_id: "ADDR_99",
                email_domain: "risk.com",
                neighbor_count: 12
            })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('report-content').innerHTML = `
                <div class="risk-card">
                    <p class="risk-tag">判定结果：${data.is_fraud ? '拦截' : '放行'}</p>
                    <p>风险评分：${data.risk_score * 100}%</p>
                    <hr>
                    <p><strong>AI 专家意见：</strong></p>
                    <p>${data.analysis_report}</p>
                </div>
            `;
        });
    }
});