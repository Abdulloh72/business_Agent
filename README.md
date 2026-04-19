# Sales Data Analyzer Agent 📊

Ushbu ilova foydalanuvchilarga savdo ma'lumotlarini (CSV/Excel formatida) yuklab, vizuallashtirish va sun'iy intellekt agentiga ma'lumotlar ustida tabiiy tilda savollar berish imkoniyatini taqdim etadi.

## Mahalliy ishga tushirish (Local Run)

1. Kerakli kutubxonalarni o'rnating:
   `pip install -r requirements.txt`
2. Streamlit serverini ishga tushiring:
   `streamlit run app.py`

## Streamlit Cloud orqali Deploy qilish (Live URL)

Dasturni Streamlit Cloud orqali butun dunyodan foydalanish mumkin bo'lgan jonli manzil (Live URL) ko'rinishida chiqarish uchun quyidagi ko'rsatmalarni bajaring:

### 1-qadam: Loyihani GitHub'ga yuklash
Ushbu papkadagi barcha kodlarni (`app.py`, `requirements.txt`, `.gitignore`) o'zingizning shaxsiy GitHub hisobingizda yangi public (yoki private) repozitoriya ochib, unga Push qiling.

### 2-qadam: Streamlit Cloud'da o'rnatish
1. [share.streamlit.io](https://share.streamlit.io/) veb-saytiga kiring va GitHub orqali ro'yxatdan o'ting.
2. **"New app"** (Yangi ilova) tugmasini bosing.
3. Loyiha papkasini joylashtirgan GitHub repozitoriyangizni tanlang.
4. Branch sifatida masalan `main` ni tanlang.
5. "Main file path" qatorida asosiy faylimiz nomini **`app.py`** deb yozing.
6. **"Deploy!"** tugmasini bosing.

Ilovingiz bir-ikki daqiqada tayyor bo'ladi va ekranda uni **Public URL** silkasi paydo bo'ladi. Ushbu silkani do'stlaringizga ham ulashishingiz mumkin!
