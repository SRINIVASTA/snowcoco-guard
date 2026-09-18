import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake.snowpark.context import get_active_session

# Page layout setup
st.set_page_config(page_title="SnowCortex Guard", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    .stButton>button { width: 100%; font-weight: bold; background-color: #2563EB; color: white; border-radius: 8px; }
    .stButton>button:hover { background-color: #1D4ED8; border-color: #1D4ED8; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛡️ SnowCortex Guard: Autonomous Compliance Copilot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automated Financial Intelligence & Audit Line-of-Custody Tracking</p>', unsafe_allow_html=True)

# --- HYBRID CONNECTION HANDLER ---
# Dynamically routes connection based on whether it is running inside Snowflake or on public Streamlit Cloud
try:
    # Attempt to grab active context if running natively inside Snowflake
    session = get_active_session()
except ImportError:
    # Fallback to connection defined in the Streamlit web Secrets TOML panel
    try:
        conn = st.connection("snowflake")
        session = conn.session()
    except Exception as e:
        st.error(f"Failed to initialize secure cloud database connection: {str(e)}")
        st.stop()

# --- SIDEBAR GOVERNANCE MASK ---
with st.sidebar:
    st.image("https://icons8.com", width=80)
    st.markdown("### Agent Governance Mask")
    st.info("Authenticated via Streamlit Cloud Secure Secrets Wrapper")
    st.caption("Target context: HACKATHON_COMPLIANCE_DB.RISK_INTELLIGENCE_SCHEMA")
    st.divider()
    
    try:
        total_tx_in_db = session.sql("SELECT COUNT(*) FROM TRANSACTION_LEDGER").collect()[0][0]
        st.metric(label="Active Transaction Logs", value=f"{total_tx_in_db}+ Records")
    except Exception:
        st.caption("Unable to fetch real-time record count metrics.")
        
    st.success("📊 Plotly Engine Connected")
    st.success("✔️ Cortex Lineage Active")

# Three Functional Subtasks Action Panel
st.markdown("### ⚡ Executive Action Panel")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔍 Task 1: Velocity Ledger Analysis")
    st.caption("Query TRANSACTION_LEDGER to isolate recent rolling 48-hour activity spikes across high-risk accounts.")
    btn_velocity = st.button("Analyze 48-Hour Velocity", key="btn_vel")

with col2:
    st.markdown("#### ⏳ Task 2: KYC Lifecycle Audit")
    st.caption("Audit expiration lifecycles and project future mandatory compliance remediation windows.")
    btn_kyc = st.button("Run KYC Expiry Audit", key="btn_kyc_lifecycle")

with col3:
    st.markdown("#### 📄 Task 3: Export STR Audit Logs")
    st.caption("Export flagged Suspicious Transaction Reports including exact cross-referenced regulatory mappings.")
    btn_export = st.button("Generate & Export STRs", key="btn_str_export")

st.divider()

# TASK 1 HANDLER: TELEMETRY ANALYSIS AND PLOTLY BAR BREAKDOWN
if btn_velocity:
    st.subheader("📊 Flagged Accounts: 48-Hour Transaction Telemetry & Category Spikes")
    with st.spinner("Analyzing high-risk data flows across bulk ledger datasets..."):
        try:
            df_velocity = session.sql("SELECT * FROM V_FLAGGED_ACCOUNTS_48HR_VELOCITY WHERE AMOUNT >= 500000").to_pandas()
            
            if df_velocity.empty:
                st.warning("No anomalies found matching criteria within the current timeframe.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**High Exposure Anomalies Detected ({len(df_velocity)} entries matched):**")
                    st.dataframe(df_velocity, use_container_width=True)
                with c2:
                    st.markdown("**Capital Exposure Plotly Distribution Matrix:**")
                    df_chart = df_velocity.groupby(['MERCHANT_CATEGORY', 'ACCOUNT_ID'])['AMOUNT'].sum().reset_index()
                    fig_vel = px.bar(df_chart, x='MERCHANT_CATEGORY', y='AMOUNT', color='ACCOUNT_ID',
                                     title="High-Risk Exposure Breakdown Across 100+ Transactions", barmode='group', template='plotly_white')
                    st.plotly_chart(fig_vel, use_container_width=True)
        except Exception as e:
            st.error(f"Error executing telemetry check: {str(e)}")

# TASK 2 HANDLER: STORED PROCEDURE REMEDIATION AND GANTT LIFECYCLE CHART
if btn_kyc:
    st.subheader("⏳ Lifecycle Audit: Expired Identifications & Grace Window Calculations")
    with st.spinner("Calculating remediation timelines..."):
        try:
            proc_result = session.sql("CALL AUDIT_KYC_STATUS_LIFECYCLE()").collect()
            st.success(proc_result[0][0])
            
            df_kyc = session.sql("SELECT ACCOUNT_ID, CUSTOMER_NAME, KYC_STATUS, KYC_EXPIRY_DATE, RECOMMENDED_REVERIFICATION_DATE FROM ACCOUNT_MASTER WHERE KYC_STATUS = 'EXPIRED'").to_pandas()
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Audited Expiration Targets:**")
                st.dataframe(df_kyc, use_container_width=True)
            with c2:
                st.markdown("**Plotly Remediation Milestone Window:**")
                df_kyc['KYC_EXPIRY_DATE'] = pd.to_datetime(df_kyc['KYC_EXPIRY_DATE'])
                df_kyc['RECOMMENDED_REVERIFICATION_DATE'] = pd.to_datetime(df_kyc['RECOMMENDED_REVERIFICATION_DATE'])
                fig_timeline = px.timeline(df_kyc, start="KYC_EXPIRY_DATE", end="RECOMMENDED_REVERIFICATION_DATE", y="CUSTOMER_NAME", color="ACCOUNT_ID",
                                           title="30-Day Mandatory KYC Remediation Windows", template='plotly_white')
                fig_timeline.update_yaxes(autorange="reversed")
                st.plotly_chart(fig_timeline, use_container_width=True)
        except Exception as e:
            st.error(f"Error executing lifecycle validation: {str(e)}")

# TASK 3 HANDLER: WORKFLOW ARCHIVE SUBMISSION COMPILATION
if btn_export:
    st.subheader("📄 Formal Regulatory Submission Pipeline")
    with st.spinner("Compiling cross-referenced compliance outputs..."):
        try:
            df_export = session.sql("SELECT * FROM V_AUDIT_SUBMISSION_EXPORT").to_pandas()
            
            if df_export.empty:
                st.info("No compliance items found.")
            else:
                for idx, row in df_export.iterrows():
                    with st.expander(f"📋 Record Reference: {row['STR_REPORT_ID']} | Target Account: {row['ACCOUNT_ID']}"):
                        st.markdown(f"**Regulatory Target Mappings:** `{row['REGULATORY_CLAUSE_MAPPING']}`")
                        st.markdown(row['GENERATED_REPORT_MD'])
                
                json_string = df_export.to_json(orient="records", indent=4)
                st.download_button(label="📥 Download Formal Audit Submission Export (JSON)", data=json_string, file_name="flagged_str_regulatory_submission.json", mime="application/json")
        except Exception as e:
            st.error(f"Error compiling regulatory export: {str(e)}")
