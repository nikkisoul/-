# -*- coding: utf-8 -*-
"""
供应链物料时间差距分析工具 - 主应用程序
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 页面配置
st.set_page_config(
    page_title="供应链物料时间差距分析工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'procurement_plans' not in st.session_state:
    st.session_state.procurement_plans = pd.DataFrame()
if 'contracts' not in st.session_state:
    st.session_state.contracts = pd.DataFrame()
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame()
if 'deliveries' not in st.session_state:
    st.session_state.deliveries = pd.DataFrame()
if 'inspection_queue' not in st.session_state:
    st.session_state.inspection_queue = pd.DataFrame()
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame()
if 'delivered_materials' not in st.session_state:
    st.session_state.delivered_materials = pd.DataFrame()
if 'returned_materials' not in st.session_state:
    st.session_state.returned_materials = pd.DataFrame()
if 'batch_info' not in st.session_state:
    st.session_state.batch_info = pd.DataFrame()
if 'material_batch_mapping' not in st.session_state:
    st.session_state.material_batch_mapping = pd.DataFrame()

# 辅助函数
def calculate_days_difference(demand_date, delivery_date):
    """计算需求日期与到货日期之间的天数差距"""
    if pd.isna(demand_date) or pd.isna(delivery_date):
        return None
    return (delivery_date - demand_date).days

def calculate_batch_completion_rate(batch_id, materials_data):
    """计算指定架次的物料完成率"""
    if materials_data.empty:
        return 0
    
    batch_materials = materials_data[materials_data['架次'] == batch_id]
    if batch_materials.empty:
        return 0
    
    total_required = batch_materials['需求数量'].sum()
    total_delivered = batch_materials['已到货数量'].fillna(0).sum()
    
    if total_required == 0:
        return 0
    
    return (total_delivered / total_required) * 100

def create_sample_data():
    """创建示例数据"""
    # 示例采购计划数据
    sample_plans = pd.DataFrame({
        '计划编号': ['P001', 'P002', 'P003', 'P004', 'P005'],
        '物料编号': ['M001', 'M002', 'M003', 'M001', 'M004'],
        '物料名称': ['螺栓A', '螺母B', '垫片C', '螺栓A', '轴承D'],
        '物料类型': ['紧固件', '紧固件', '密封件', '紧固件', '传动件'],
        '供应商': ['供应商A', '供应商B', '供应商A', '供应商C', '供应商B'],
        '架次': ['001', '001', '002', '002', '003'],
        '需求数量': [1000, 500, 200, 800, 100],
        '计划下达日期': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-05', '2024-01-08', '2024-01-10']),
        '需求日期': pd.to_datetime(['2024-02-01', '2024-02-01', '2024-02-15', '2024-02-15', '2024-03-01'])
    })
    
    # 示例到货数据
    sample_deliveries = pd.DataFrame({
        '到货编号': ['D001', 'D002', 'D003', 'D004', 'D005'],
        '物料编号': ['M001', 'M002', 'M003', 'M001', 'M004'],
        '架次': ['001', '001', '002', '002', '003'],
        '已到货数量': [1000, 500, 200, 600, 80],
        '实际到货日期': pd.to_datetime(['2024-02-05', '2024-01-28', '2024-02-20', '2024-02-18', '2024-03-05'])
    })
    
    return sample_plans, sample_deliveries

# 侧边栏
st.sidebar.title("📊 供应链分析工具")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "导航菜单",
    ["🏠 首页概览", "📥 数据管理", "📈 时间差距分析", "🎯 架次分析", "⚙️ 供应链环节分析", "📊 报告导出"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 快速操作")
if st.sidebar.button("📝 加载示例数据"):
    sample_plans, sample_deliveries = create_sample_data()
    st.session_state.procurement_plans = sample_plans
    st.session_state.deliveries = sample_deliveries
    st.session_state.data_loaded = True
    st.sidebar.success("✅ 示例数据已加载！")

# 主页面内容
if page == "🏠 首页概览":
    st.title("🏠 供应链物料时间差距分析工具")
    st.markdown("### 欢迎使用供应链数据分析平台")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📥 **数据管理**\n\n上传或输入物料需求和到货数据")
    with col2:
        st.success("📈 **时间差距分析**\n\n可视化需求与到货时间差距")
    with col3:
        st.warning("🎯 **架次分析**\n\n追踪各架次物料完成情况")
    
    st.markdown("---")
    
    if st.session_state.data_loaded:
        st.markdown("### 📊 关键指标概览")
        
        # 合并数据进行分析
        if not st.session_state.procurement_plans.empty and not st.session_state.deliveries.empty:
            merged_data = pd.merge(
                st.session_state.procurement_plans,
                st.session_state.deliveries,
                on=['物料编号', '架次'],
                how='left'
            )
            
            # 计算天数差距
            merged_data['天数差距'] = merged_data.apply(
                lambda row: calculate_days_difference(row['需求日期'], row['实际到货日期']),
                axis=1
            )
            
            # 显示关键指标
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_diff = merged_data['天数差距'].mean()
                st.metric("平均时间差距", f"{avg_diff:.1f} 天" if not pd.isna(avg_diff) else "N/A")
            
            with col2:
                on_time_rate = (merged_data['天数差距'] <= 0).sum() / len(merged_data) * 100
                st.metric("按时到货率", f"{on_time_rate:.1f}%")
            
            with col3:
                total_materials = len(merged_data)
                st.metric("物料总数", f"{total_materials}")
            
            with col4:
                total_batches = merged_data['架次'].nunique()
                st.metric("架次总数", f"{total_batches}")
            
            # 简单的可视化
            st.markdown("### 📈 时间差距分布")
            fig = px.histogram(
                merged_data.dropna(subset=['天数差距']),
                x='天数差距',
                nbins=20,
                title="物料到货时间差距分布",
                labels={'天数差距': '时间差距(天)', 'count': '物料数量'}
            )
            fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="按时交付线")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 请从侧边栏加载示例数据或前往【数据管理】页面上传数据")

elif page == "📥 数据管理":
    st.title("📥 数据管理")
    
    tab1, tab2, tab3 = st.tabs(["📤 数据上传", "✏️ 手动输入", "🗂️ 架次管理"])
    
    with tab1:
        st.markdown("### 📤 批量数据上传")
        st.markdown("上传Excel或CSV文件以导入数据")
        
        # 添加文件格式说明
        with st.expander("📋 查看文件格式要求"):
            st.markdown("""
            **采购计划数据应包含以下列:**
            - 计划编号, 物料编号, 物料名称, 物料类型, 供应商, 架次, 需求数量, 需求日期
            
            **到货数据应包含以下列:**
            - 到货编号, 物料编号, 架次, 已到货数量, 实际到货日期
            
            **注意事项:**
            - 支持CSV和Excel(.xlsx)格式
            - 文件大小不超过200MB
            - 日期格式建议: YYYY-MM-DD (例如: 2024-01-01)
            - 确保文件编码为UTF-8(CSV文件)
            """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 采购计划数据")
            uploaded_plans = st.file_uploader(
                "上传采购计划",
                type=['csv', 'xlsx', 'xls'],
                key='plans_upload',
                help="支持CSV和Excel格式，最大200MB"
            )
            
            if uploaded_plans is not None:
                try:
                    # 显示文件信息
                    file_details = {
                        "文件名": uploaded_plans.name,
                        "文件大小": f"{uploaded_plans.size / 1024:.2f} KB",
                        "文件类型": uploaded_plans.type
                    }
                    st.info(f"📄 正在处理: {uploaded_plans.name}")
                    
                    # 读取文件
                    if uploaded_plans.name.endswith('.csv'):
                        # 尝试不同的编码
                        try:
                            df = pd.read_csv(uploaded_plans, encoding='utf-8')
                        except UnicodeDecodeError:
                            uploaded_plans.seek(0)  # 重置文件指针
                            df = pd.read_csv(uploaded_plans, encoding='gbk')
                    elif uploaded_plans.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(uploaded_plans, engine='openpyxl')
                    else:
                        st.error("❌ 不支持的文件格式")
                        df = None
                    
                    if df is not None:
                        # 验证必要的列
                        required_cols = ['物料编号', '架次']
                        missing_cols = [col for col in required_cols if col not in df.columns]
                        
                        if missing_cols:
                            st.warning(f"⚠️ 缺少必要的列: {', '.join(missing_cols)}")
                            st.info("当前文件包含的列:")
                            st.write(list(df.columns))
                        
                        # 保存到session state
                        st.session_state.procurement_plans = df
                        st.session_state.data_loaded = True
                        st.success(f"✅ 成功上传 {len(df)} 条采购计划记录")
                        
                        # 显示数据预览
                        st.markdown("**数据预览:**")
                        st.dataframe(df.head(10))
                        
                        # 显示数据统计
                        st.markdown("**数据统计:**")
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("总记录数", len(df))
                        with col_b:
                            st.metric("列数", len(df.columns))
                        with col_c:
                            if '架次' in df.columns:
                                st.metric("架次数", df['架次'].nunique())
                        
                except Exception as e:
                    st.error(f"❌ 上传失败: {str(e)}")
                    st.error(f"错误类型: {type(e).__name__}")
                    
                    # 提供详细的错误信息
                    if "openpyxl" in str(e):
                        st.warning("💡 提示: 请确保已安装openpyxl库。运行: pip install openpyxl")
                    elif "encoding" in str(e).lower():
                        st.warning("💡 提示: 文件编码问题。请确保CSV文件使用UTF-8或GBK编码")
                    
                    # 显示详细错误信息（调试用）
                    with st.expander("查看详细错误信息"):
                        st.code(str(e))
        
        with col2:
            st.markdown("#### 到货数据")
            uploaded_deliveries = st.file_uploader(
                "上传到货数据",
                type=['csv', 'xlsx', 'xls'],
                key='deliveries_upload',
                help="支持CSV和Excel格式，最大200MB"
            )
            
            if uploaded_deliveries is not None:
                try:
                    # 显示文件信息
                    st.info(f"📄 正在处理: {uploaded_deliveries.name}")
                    
                    # 读取文件
                    if uploaded_deliveries.name.endswith('.csv'):
                        # 尝试不同的编码
                        try:
                            df = pd.read_csv(uploaded_deliveries, encoding='utf-8')
                        except UnicodeDecodeError:
                            uploaded_deliveries.seek(0)  # 重置文件指针
                            df = pd.read_csv(uploaded_deliveries, encoding='gbk')
                    elif uploaded_deliveries.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(uploaded_deliveries, engine='openpyxl')
                    else:
                        st.error("❌ 不支持的文件格式")
                        df = None
                    
                    if df is not None:
                        # 验证必要的列
                        required_cols = ['物料编号', '架次']
                        missing_cols = [col for col in required_cols if col not in df.columns]
                        
                        if missing_cols:
                            st.warning(f"⚠️ 缺少必要的列: {', '.join(missing_cols)}")
                            st.info("当前文件包含的列:")
                            st.write(list(df.columns))
                        
                        # 保存到session state
                        st.session_state.deliveries = df
                        st.session_state.data_loaded = True
                        st.success(f"✅ 成功上传 {len(df)} 条到货记录")
                        
                        # 显示数据预览
                        st.markdown("**数据预览:**")
                        st.dataframe(df.head(10))
                        
                        # 显示数据统计
                        st.markdown("**数据统计:**")
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("总记录数", len(df))
                        with col_b:
                            st.metric("列数", len(df.columns))
                        with col_c:
                            if '架次' in df.columns:
                                st.metric("架次数", df['架次'].nunique())
                        
                except Exception as e:
                    st.error(f"❌ 上传失败: {str(e)}")
                    st.error(f"错误类型: {type(e).__name__}")
                    
                    # 提供详细的错误信息
                    if "openpyxl" in str(e):
                        st.warning("💡 提示: 请确保已安装openpyxl库。运行: pip install openpyxl")
                    elif "encoding" in str(e).lower():
                        st.warning("💡 提示: 文件编码问题。请确保CSV文件使用UTF-8或GBK编码")
                    
                    # 显示详细错误信息（调试用）
                    with st.expander("查看详细错误信息"):
                        st.code(str(e))
    
    with tab2:
        st.markdown("### ✏️ 手动输入数据")
        
        input_type = st.selectbox("选择输入类型", ["采购计划", "到货记录"])
        
        if input_type == "采购计划":
            with st.form("plan_form"):
                col1, col2 = st.columns(2)
                with col1:
                    plan_id = st.text_input("计划编号")
                    material_id = st.text_input("物料编号")
                    material_name = st.text_input("物料名称")
                    material_type = st.text_input("物料类型")
                with col2:
                    supplier = st.text_input("供应商")
                    batch = st.text_input("架次")
                    quantity = st.number_input("需求数量", min_value=0, value=0)
                    demand_date = st.date_input("需求日期")
                
                submitted = st.form_submit_button("➕ 添加采购计划")
                if submitted:
                    new_plan = pd.DataFrame({
                        '计划编号': [plan_id],
                        '物料编号': [material_id],
                        '物料名称': [material_name],
                        '物料类型': [material_type],
                        '供应商': [supplier],
                        '架次': [batch],
                        '需求数量': [quantity],
                        '需求日期': [pd.to_datetime(demand_date)]
                    })
                    st.session_state.procurement_plans = pd.concat([st.session_state.procurement_plans, new_plan], ignore_index=True)
                    st.session_state.data_loaded = True
                    st.success("✅ 采购计划已添加！")
        
        else:  # 到货记录
            with st.form("delivery_form"):
                col1, col2 = st.columns(2)
                with col1:
                    delivery_id = st.text_input("到货编号")
                    material_id = st.text_input("物料编号")
                    batch = st.text_input("架次")
                with col2:
                    delivered_qty = st.number_input("已到货数量", min_value=0, value=0)
                    delivery_date = st.date_input("实际到货日期")
                
                submitted = st.form_submit_button("➕ 添加到货记录")
                if submitted:
                    new_delivery = pd.DataFrame({
                        '到货编号': [delivery_id],
                        '物料编号': [material_id],
                        '架次': [batch],
                        '已到货数量': [delivered_qty],
                        '实际到货日期': [pd.to_datetime(delivery_date)]
                    })
                    st.session_state.deliveries = pd.concat([st.session_state.deliveries, new_delivery], ignore_index=True)
                    st.session_state.data_loaded = True
                    st.success("✅ 到货记录已添加！")
    
    with tab3:
        st.markdown("### 🗂️ 架次管理")
        st.markdown("管理物料有效起始架次信息")
        
        with st.form("batch_form"):
            col1, col2 = st.columns(2)
            with col1:
                material_id = st.text_input("物料编号")
                material_name = st.text_input("物料名称")
            with col2:
                start_batch = st.text_input("有效起始架次")
                end_batch = st.text_input("有效结束架次（可选）")
            
            submitted = st.form_submit_button("➕ 添加架次映射")
            if submitted:
                new_mapping = pd.DataFrame({
                    '物料编号': [material_id],
                    '物料名称': [material_name],
                    '有效起始架次': [start_batch],
                    '有效结束架次': [end_batch if end_batch else None]
                })
                st.session_state.material_batch_mapping = pd.concat([st.session_state.material_batch_mapping, new_mapping], ignore_index=True)
                st.success("✅ 架次映射已添加！")
        
        if not st.session_state.material_batch_mapping.empty:
            st.markdown("#### 当前架次映射")
            st.dataframe(st.session_state.material_batch_mapping)

elif page == "📈 时间差距分析":
    st.title("📈 物料需求与到货时间差距分析")
    
    if (not st.session_state.data_loaded) and st.session_state.procurement_plans.empty:
        st.warning("⚠️ 请先在【数据管理】页面上传或输入数据")
    else:
        # 合并数据
        merged_data = pd.merge(
            st.session_state.procurement_plans,
            st.session_state.deliveries,
            on=['物料编号', '架次'],
            how='left'
        )
        
        # 计算天数差距
        merged_data['天数差距'] = merged_data.apply(
            lambda row: calculate_days_difference(row['需求日期'], row['实际到货日期']),
            axis=1
        )
        
        # 筛选选项
        st.markdown("### 🔍 筛选条件")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.selectbox("筛选类型", ["全部数据", "仅延迟", "仅按时/提前"])
        with col2:
            if '供应商' in merged_data.columns:
                suppliers = ['全部'] + list(merged_data['供应商'].unique())
                selected_supplier = st.selectbox("供应商", suppliers)
        with col3:
            if '物料类型' in merged_data.columns:
                material_types = ['全部'] + list(merged_data['物料类型'].unique())
                selected_type = st.selectbox("物料类型", material_types)
        
        # 应用筛选
        filtered_data = merged_data.copy()
        if filter_type == "仅延迟":
            filtered_data = filtered_data[filtered_data['天数差距'] > 0]
        elif filter_type == "仅按时/提前":
            filtered_data = filtered_data[filtered_data['天数差距'] <= 0]
        
        if selected_supplier != '全部':
            filtered_data = filtered_data[filtered_data['供应商'] == selected_supplier]
        if selected_type != '全部':
            filtered_data = filtered_data[filtered_data['物料类型'] == selected_type]
        
        # 统计摘要
        st.markdown("### 📊 统计摘要")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_diff = filtered_data['天数差距'].mean()
            st.metric("平均时间差距", f"{avg_diff:.1f} 天" if not pd.isna(avg_diff) else "N/A")
        with col2:
            max_delay = filtered_data['天数差距'].max()
            st.metric("最大延迟", f"{max_delay:.0f} 天" if not pd.isna(max_delay) else "N/A")
        with col3:
            min_diff = filtered_data['天数差距'].min()
            st.metric("最早到货", f"{min_diff:.0f} 天" if not pd.isna(min_diff) else "N/A")
        with col4:
            on_time_count = (filtered_data['天数差距'] <= 0).sum()
            on_time_rate = on_time_count / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
            st.metric("按时到货率", f"{on_time_rate:.1f}%")
        
        # 可视化
        st.markdown("### 📊 可视化分析")
        
        tab1, tab2, tab3 = st.tabs(["条形图", "分布图", "趋势图"])
        
        with tab1:
            # 按物料分组的时间差距条形图
            if not filtered_data.empty:
                fig = px.bar(
                    filtered_data.groupby('物料名称')['天数差距'].mean().reset_index(),
                    x='物料名称',
                    y='天数差距',
                    title="各物料平均时间差距",
                    labels={'天数差距': '平均时间差距(天)', '物料名称': '物料'},
                    color='天数差距',
                    color_continuous_scale='RdYlGn_r'
                )
                fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="按时交付线")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # 时间差距分布直方图
            if not filtered_data.dropna(subset=['天数差距']).empty:
                fig = px.histogram(
                    filtered_data.dropna(subset=['天数差距']),
                    x='天数差距',
                    nbins=30,
                    title="时间差距分布",
                    labels={'天数差距': '时间差距(天)', 'count': '数量'}
                )
                fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="按时交付线")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # 时间趋势图
            if not filtered_data.dropna(subset=['需求日期', '天数差距']).empty:
                trend_data = filtered_data.dropna(subset=['需求日期', '天数差距']).sort_values('需求日期')
                fig = px.line(
                    trend_data,
                    x='需求日期',
                    y='天数差距',
                    title="时间差距趋势",
                    labels={'需求日期': '需求日期', '天数差距': '时间差距(天)'},
                    markers=True
                )
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        # 详细数据表
        st.markdown("### 📋 详细数据")
        st.dataframe(filtered_data[['物料编号', '物料名称', '供应商', '架次', '需求日期', '实际到货日期', '天数差距']])

elif page == "🎯 架次分析":
    st.title("🎯 架次物料完成情况分析")
    
    if (not st.session_state.data_loaded) and st.session_state.procurement_plans.empty:
        st.warning("⚠️ 请先在【数据管理】页面上传或输入数据")
    else:
        # 合并数据
        merged_data = pd.merge(
            st.session_state.procurement_plans,
            st.session_state.deliveries,
            on=['物料编号', '架次'],
            how='left'
        )
        
        # 填充缺失的到货数量为0
        merged_data['已到货数量'] = merged_data['已到货数量'].fillna(0)
        
        # 计算完成率
        merged_data['完成率'] = (merged_data['已到货数量'] / merged_data['需求数量'] * 100).round(2)
        
        # 架次选择
        batches = sorted(merged_data['架次'].unique())
        selected_batch = st.selectbox("选择架次", batches)
        
        # 筛选选定架次的数据
        batch_data = merged_data[merged_data['架次'] == selected_batch]
        
        # 架次概览
        st.markdown(f"### 📊 架次 {selected_batch} 概览")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_materials = len(batch_data)
            st.metric("物料种类数", f"{total_materials}")
        
        with col2:
            total_required = batch_data['需求数量'].sum()
            st.metric("总需求数量", f"{total_required:,.0f}")
        
        with col3:
            total_delivered = batch_data['已到货数量'].sum()
            st.metric("总到货数量", f"{total_delivered:,.0f}")
        
        with col4:
            overall_completion = (total_delivered / total_required * 100) if total_required > 0 else 0
            st.metric("整体完成率", f"{overall_completion:.1f}%")
        
        # 完成率仪表盘
        st.markdown("### 🎯 架次完成率仪表盘")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_completion,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"架次 {selected_batch} 完成率"},
            delta={'reference': 100, 'suffix': '%'},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightcoral"},
                    {'range': [50, 80], 'color': "lightyellow"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 物料完成情况详细图表
        st.markdown("### 📊 各物料完成情况")
        
        fig = px.bar(
            batch_data,
            x='物料名称',
            y=['需求数量', '已到货数量'],
            title=f"架次 {selected_batch} 各物料需求与到货对比",
            labels={'value': '数量', '物料名称': '物料'},
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 完成率分布
        fig = px.bar(
            batch_data,
            x='物料名称',
            y='完成率',
            title=f"架次 {selected_batch} 各物料完成率",
            labels={'完成率': '完成率(%)', '物料名称': '物料'},
            color='完成率',
            color_continuous_scale='RdYlGn'
        )
        fig.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="100%完成线")
        st.plotly_chart(fig, use_container_width=True)
        
        # 详细数据表
        st.markdown("### 📋 详细物料清单")
        st.dataframe(batch_data[['物料编号', '物料名称', '供应商', '需求数量', '已到货数量', '完成率']])

elif page == "⚙️ 供应链环节分析":
    st.title("⚙️ 供应链各环节时间消耗分析")
    
    st.info("💡 此功能需要完整的供应链数据（采购计划、合同签订、订单签收、到货等）")
    
    # 这里可以添加供应链环节分析的代码
    st.markdown("### 📊 供应链环节时间分析")
    st.markdown("功能开发中...")

elif page == "📊 报告导出":
    st.title("📊 数据报告导出")
    
    if (not st.session_state.data_loaded) and st.session_state.procurement_plans.empty:
        st.warning("⚠️ 请先在【数据管理】页面上传或输入数据")
    else:
        st.markdown("### 📥 导出选项")
        
        export_type = st.selectbox("选择导出类型", ["时间差距分析报告", "架次完成情况报告", "综合分析报告"])
        
        if st.button("📥 生成并下载报告"):
            # 合并数据
            merged_data = pd.merge(
                st.session_state.procurement_plans,
                st.session_state.deliveries,
                on=['物料编号', '架次'],
                how='left'
            )
            
            # 计算天数差距
            merged_data['天数差距'] = merged_data.apply(
                lambda row: calculate_days_difference(row['需求日期'], row['实际到货日期']),
                axis=1
            )
            
            # 转换为CSV
            csv = merged_data.to_csv(index=False, encoding='utf-8-sig')
            
            st.download_button(
                label="📥 下载CSV报告",
                data=csv,
                file_name=f"供应链分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            st.success("✅ 报告已生成，点击上方按钮下载")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    供应链物料时间差距分析工具 v1.0 | © 2024
    </div>
    """,
    unsafe_allow_html=True
)
