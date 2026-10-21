import streamlit as st
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(page_title="人事工作台", page_icon="👥", layout="wide")

# 初始化 Session State 用于存储数据（模拟数据库）
if "employees" not in st.session_state:
    st.session_state.employees = pd.DataFrame([
        {
            "员工编号": "EMP001",
            "姓名": "张三",
            "性别": "男",
            "所属部门": "技术部",
            "岗位职务": "前端开发",
            "职级": "P5",
            "入职日期": "2025-03-01",
            "员工状态": "在职",
            "手机号码": "13800138000",
            "邮箱": "zhangsan@example.com"
        },
        {
            "员工编号": "EMP002",
            "姓名": "李四",
            "性别": "女",
            "所属部门": "产品部",
            "岗位职务": "产品经理",
            "职级": "P6",
            "入职日期": "2024-07-15",
            "员工状态": "在职",
            "手机号码": "13700137000",
            "邮箱": "lisi@example.com"
        }
    ])

st.title("🏢 员工花名册与入职信息工作台")

# 侧边栏导航
menu = st.sidebar.selectbox("选择功能页面", ["📊 数据总览看板", "📋 员工花名册", "📝 新员工入职登记"])

df = st.session_state.employees

# 1. 数据总览看板
if menu == "📊 数据总览看板":
    st.subheader("公司人力数据看板")
    
    col1, col2, col3 = st.columns(3)
    total_count = len(df)
    active_count = len(df[df["员工状态"] == "在职"])
    probation_count = len(df[df["员工状态"] == "试用期"])
    
    col1.metric("总员工数", f"{total_count} 人")
    col2.metric("在职人数", f"{active_count} 人")
    col3.metric("试用期人数", f"{probation_count} 人")
    
    st.divider()
    
    # 部门分布统计
    st.markdown("### 各部门人数分布")
    if not df.empty:
        dept_counts = df["所属部门"].value_counts()
        st.bar_chart(dept_counts)
    else:
        st.info("暂无数据")

# 2. 员工花名册
elif menu == "📋 员工花名册":
    st.subheader("员工花名册管理")
    
    # 搜索与过滤
    col1, col2 = st.columns(2)
    search_query = col1.text_input("🔍 搜索员工姓名/编号", "")
    status_filter = col2.selectbox("筛选员工状态", ["全部", "在职", "试用期", "离职"])
    
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["姓名"].str.contains(search_query, na=False) | 
            filtered_df["员工编号"].str.contains(search_query, na=False)
        ]
    if status_filter != "全部":
        filtered_df = filtered_df[filtered_df["员工状态"] == status_filter]
        
    st.dataframe(filtered_df, use_container_width=True)
    
    # 导出 CSV 按钮
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 导出当前筛选数据为 CSV",
        data=csv,
        file_name='employee_roster.csv',
        mime='text/csv',
    )

# 3. 新员工入职登记
elif menu == "📝 新员工入职登记":
    st.subheader("新员工入职信息录入")
    
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        
        emp_id = col1.text_input("员工编号 (如 EMP003)")
        name = col2.text_input("员工姓名")
        
        gender = col1.selectbox("性别", ["男", "女"])
        department = col2.selectbox("所属部门", ["技术部", "产品部", "运营部", "人事行政", "财务部", "市场部"])
        
        position = col1.text_input("岗位职务")
        level = col2.text_input("职级 (如 P5/M1)")
        
        hire_date = col1.date_input("入职日期", datetime.today())
        status = col2.selectbox("员工状态", ["试用期", "在职"])
        
        phone = col1.text_input("手机号码")
        email = col2.text_input("电子邮箱")
        
        submitted = st.form_submit_button("确认提交入职信息")
        
        if submitted:
            if not emp_id or not name:
                st.error("请填写员工编号和姓名！")
            else:
                new_row = {
                    "员工编号": emp_id,
                    "姓名": name,
                    "性别": gender,
                    "所属部门": department,
                    "岗位职务": position,
                    "职级": level,
                    "入职日期": str(hire_date),
                    "员工状态": status,
                    "手机号码": phone,
                    "邮箱": email
                }
                # 追加到 session state
                st.session_state.employees = pd.concat([st.session_state.employees, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"成功为 {name} 添加花名册与入职档案！")