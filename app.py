import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="Sales Data Analyzer", page_icon="📊", layout="wide")

st.title("📊 Sales Data Analyzer Agent")
st.markdown("""
Ushbu ilova yordamida siz o'zingizning savdo ma'lumotlaringizni (CSV/Excel) yuklab, ularni tahlil qilish va
sun'iy intellektga savollar berish orqali ma'lumotlar olishingiz mumkin.
""")

# OpenAI API Key Input for deployment
with st.sidebar:
    st.header("⚙️ Sozlamalar")
    st.markdown("Xavfsizlik nuqtai nazaridan, ilova hozirda Sizning shaxsiy OpenAI API kalitingiz yordamida ishlaydi.")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="sk- bilan boshlanuvchi OpenAI API kalitingizni yozasiz. (Ushbu ma'lumot sayt xotirasida xavsiz saqlanadi)")
    if not openai_api_key:
        st.warning("Agent javob qaytarishi uchun API kalitini kiritishingiz kerak.")
    
    st.markdown("---")
    st.markdown("### Deployment haqida")
    st.info("Ilova Streamlit Cloud orqali ommaga (Public) deploy qilinishga mo'ljallangan. Agar Cloud platformada secrets.toml o'rnatilgan bo'lsa, uni kodga to'g'ridan to'g'ri integratsiya qilsa ham bo'ladi.")

uploaded_file = st.file_uploader("📥 CSV yoki Excel savdo faylini yuklang", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("Fayl muvaffaqiyatli yuklandi! 🎉")
        
        st.subheader("1. Boshlang'ich Ko'rsatkichlar", divider="gray")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Umumiy qatorlar (Rows)", df.shape[0])
        with col2:
            st.metric("Umumiy ustunlar (Cols)", df.shape[1])
            
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        with col3:
            st.metric("Raqamli ustunlar", len(numeric_cols))
        with col4:
            st.metric("Kategorik ustunlar", df.shape[1] - len(numeric_cols))
                
        st.subheader("2. Ma'lumotlarni ko'rish (Dataframe View)", divider="gray")
        st.dataframe(df.head(15), use_container_width=True)
        
        st.subheader("3. 📈 Bar Chart Vizualizatsiyasi", divider="gray")
        if len(numeric_cols) > 0 and len(df.columns) > 1:
            c1, c2 = st.columns(2)
            with c1:
                x_axis = st.selectbox("X o'qi uchu ustunni tanlang (Kategoriya/Sana)", df.columns)
            with c2:
                y_axis = st.selectbox("Y o'qi uchun ustunni tanlang (Raqamli ko'rsatkich)", numeric_cols)
                
            if st.button("Grafikni chizish 📊"):
                try:
                    if x_axis == y_axis:
                        st.warning("⚠️ Iltimos, X va Y o'qlari uchun har xil ustunlarni tanlang.")
                    else:
                        chart_data = df.groupby(x_axis)[y_axis].sum().reset_index()
                        chart_data = chart_data.sort_values(by=y_axis, ascending=False).head(15) 
                        
                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.bar(chart_data[x_axis].astype(str), chart_data[y_axis], color='#FFA500', edgecolor='black')
                        plt.xticks(rotation=45, ha='right')
                        plt.title(f"{x_axis} bo'yicha {y_axis} tahlili (Top 15)")
                        plt.grid(axis='y', linestyle='--', alpha=0.7)
                        st.pyplot(fig)
                except Exception as e:
                    st.error(f"Grafik chizishda xatolik: {e}")
        else:
            st.info("Vizualizatsiya yaratish uchun mos ustunlar yetarli emas.")

        st.subheader("4. 🤖 AI Agent - Tabiiy Tilda Savol Berish", divider="gray")
        st.markdown("Ma'lumotlaringiz haqida tabiiy tilda savol bering. **Misol:** *Eng ko'p foyda keltirgan top 3 ta mahsulotni ko'rsat.*")
        
        user_question = st.text_input("💬 Savolingizni kiriting:")
        
        if st.button("Javob Olish 🚀"):
            if user_question:
                if openai_api_key:
                    with st.spinner("Agent ma'lumotlarni tahlil qilmoqda. Iltimos, kuting..."):
                        try:
                            llm = ChatOpenAI(temperature=0.0, openai_api_key=openai_api_key, model_name="gpt-4o-mini")
                            agent = create_pandas_dataframe_agent(
                                llm, 
                                df, 
                                verbose=True, 
                                allow_dangerous_code=True,
                                agent_type="openai-tools",
                                handle_parsing_errors=True,
                                max_iterations=15
                            )
                            # Custom instruction wrapper
                            prompt = f"""
Sizning vazifangiz foydalanuvchining quyidagi savoliga ma'lumotlar bazasidan qarab tahliliy javob berishdir:
SAVOL: "{user_question}"

QOIDALAR VA QADAMLAR (BUNI ALBATTA BAJARING):
1. O'zingizga kerakli ustunlarni toping (agar 'sotuv' va 'hafta' desa, mos ustunlar dataframeda bormi tekshiring).
2. Agar tahlil natijasi bir nechta raqamlar yoki kategoriyalardan iborat bo'lsa qiziqarli Matplotlib grafik chizing (Bar yoki Line chart).
3. Grafik chizganda, MUHIM QOIDA: grafik xira va kichkina bo'lib qolmasligi uchun uni chizishdan oldin ALBATTA `plt.figure(figsize=(10, 6))` deb o'lcham bering va faylni saqlashda `plt.savefig('temp_chart.png', bbox_inches='tight', dpi=300)` buyrug'idan foydalaning. Hech qachon `plt.show()` qilmang!
4. Amalni bajarganingizdan so'ng, albatta foydalanuvchiga MATNLI JAVOB (Final Answer) qaytaring. Matn ichida raqamlarni qisqacha yozib, "Grafik tayyorlandi" deb izoh bering.
                            """
                            response = agent.run(prompt)
                            st.success("✅ Javob tayyor:")
                            st.write(response)
                            
                            if os.path.exists("temp_chart.png"):
                                st.image("temp_chart.png", caption="AI yaratgan tahlil grafigi", use_container_width=True)
                                os.remove("temp_chart.png")
                        except Exception as e:
                            st.error(f"Agent ishida xatolik yuz berdi: {e}\n\nOdatda bu noto'g'ri API kaliti yoki qiyin formatdagi jadval tufayli bo'lishi mumkin.")
                else:
                    st.error("⚠️ Iltimos, yon paneldan (sidebar) OpenAI API kalitingizni kiriting.")
            else:
                st.warning("⚠️ Iltimos, avval savol kiriting.")
                
    except Exception as e:
         st.error(f"Faylni o'qishda kutilmagan xatolik yuz berdi: {e}")
