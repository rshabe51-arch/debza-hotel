import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AUTOMATED CREDENTIALS ---
TELEGRAM_BOT_TOKEN = "8425849500:AAEqmbBH1g4pTvCYErTIQZqKRF78rneMZnk"
TELEGRAM_CHAT_ID = "7034572350"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Debza Luxury Hotel & Spa</title>
    <style>
        /* LUXURY BLACK, CHARCOAL & GOLD PALETTE */
        :root {
            --bg-dark: #0A0A0A;          /* Deep Velvet Black */
            --panel-bg: rgba(20, 20, 20, 0.88); /* Sleek Charcoal Glass */
            --accent-gold: #D4AF37;      /* Polished Champagne Gold */
            --accent-hover: #F3E5AB;     /* Soft Light Ivory Gold */
            --text-main: #FFFFFF;        /* Crisp White */
            --text-muted: #B3B3B3;       /* Elegant Silver-Gray */
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Playfair Display', 'Segoe UI', serif; }
        
        body { 
            background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)), 
                        url('https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1600') no-repeat center center fixed;
            background-size: cover;
            color: var(--text-main); 
            line-height: 1.6; 
            min-height: 100vh; 
        }
        
        header { 
            background: rgba(10, 10, 10, 0.95); 
            border-bottom: 1px solid var(--accent-gold); 
            position: sticky; 
            top: 0; 
            z-index: 1000; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.8); 
        }
        
        .nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 20px; }
        .logo { font-size: 1.8rem; font-weight: 700; color: var(--accent-gold); letter-spacing: 3px; text-transform: uppercase; }
        .nav-right { display: flex; align-items: center; gap: 20px; }
        .nav-tabs { display: flex; gap: 10px; flex-wrap: wrap; }
        
        .tab-btn { 
            background: none; 
            border: 1px solid rgba(212, 175, 55, 0.4); 
            color: var(--text-muted); 
            font-size: 0.82rem; 
            cursor: pointer; 
            padding: 8px 18px; 
            border-radius: 4px;
            text-transform: uppercase; 
            font-weight: 600; 
            letter-spacing: 1px;
            transition: all 0.3s ease; 
        }
        
        .tab-btn:hover, .tab-btn.active { 
            background: var(--accent-gold); 
            color: var(--bg-dark); 
            border-color: var(--accent-gold);
            box-shadow: 0 0 12px rgba(212, 175, 55, 0.4); 
        }

        /* LANG SWITCHER STYLE */
        .lang-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--accent-gold);
            color: var(--accent-gold);
            padding: 6px 12px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .lang-btn:hover {
            background: var(--accent-gold);
            color: var(--bg-dark);
        }
        
        .content-section { 
            max-width: 1000px; 
            margin: 50px auto; 
            padding: 40px; 
            display: none; 
            background: var(--panel-bg); 
            border-radius: 4px; 
            border: 1px solid rgba(212, 175, 55, 0.15); 
            backdrop-filter: blur(8px); 
            box-shadow: 0 20px 40px rgba(0,0,0,0.9); 
        }
        
        .content-section.active { display: block; animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .section-banner { width: 100%; height: 380px; object-fit: cover; border-radius: 2px; border: 1px solid rgba(212, 175, 55, 0.3); margin-bottom: 30px; }
        
        h2 { font-size: 2.4rem; color: var(--accent-gold); margin-bottom: 20px; letter-spacing: 2px; text-transform: uppercase; font-weight: 400; text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 25px; }
        
        .card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(212, 175, 55, 0.1); border-radius: 2px; padding: 25px; transition: all 0.3s ease; }
        .card:hover { border-color: var(--accent-gold); background: rgba(255, 255, 255, 0.06); transform: translateY(-3px); }
        .card h3 { color: var(--accent-gold); font-size: 1.4rem; margin-bottom: 12px; font-weight: 400; letter-spacing: 1px; }
        .card-img { width: 100%; height: 200px; object-fit: cover; border-radius: 2px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05); }
        
        .price { font-size: 1.2rem; color: var(--accent-gold); font-weight: bold; margin-top: 15px; display: block; border-top: 1px solid rgba(212, 175, 55, 0.2); padding-top: 10px; }
        
        .form-container { max-width: 600px; margin: 0 auto; }
        .form-group { margin-bottom: 22px; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--accent-gold); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
        .form-group input, .form-group select { width: 100%; padding: 14px; background: rgba(0, 0, 0, 0.6); border: 1px solid rgba(212, 175, 55, 0.25); color: #FFFFFF; font-size: 1rem; transition: border-color 0.3s ease; }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: var(--accent-gold); }
        
        .btn-submit { width: 100%; padding: 16px; background: var(--accent-gold); color: var(--bg-dark); border: none; font-size: 1.1rem; font-weight: 700; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; transition: all 0.3s ease; }
        .btn-submit:hover { background: var(--accent-hover); box-shadow: 0 0 15px rgba(212, 175, 55, 0.6); }
        
        footer { text-align: center; padding: 40px; color: var(--text-muted); font-size: 0.85rem; letter-spacing: 1px; }
    </style>
</head>
<body>
    <header>
        <div class="nav-container">
            <div class="logo">Debza Hotel</div>
            <div class="nav-right">
                <nav class="nav-tabs">
                    <button class="tab-btn active" id="tab-overview" onclick="switchTab('overview')">Overview</button>
                    <button class="tab-btn" id="tab-rooms" onclick="switchTab('rooms')">Suites</button>
                    <button class="tab-btn" id="tab-dining" onclick="switchTab('dining')">Dining</button>
                    <button class="tab-btn" id="tab-booking" onclick="switchTab('booking')">Reservations</button>
                </nav>
                <button class="lang-btn" onclick="toggleLanguage()" id="lang-toggle">አማርኛ</button>
            </div>
        </div>
    </header>

    <!-- OVERVIEW SECTION -->
    <div id="overview" class="content-section active">
        <img class="section-banner" src="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1200" alt="Resort Exterior">
        <h2 id="ov-title">A Sanctuary of Refinement</h2>
        <p style="color: var(--text-muted); font-size: 1.1rem; text-align: center; font-style: italic;" id="ov-subtitle">Where sovereign luxury meets the rich heritage of Gojjam.</p>
        <p style="color: var(--text-muted); margin-top: 20px; text-align: justify; line-height: 1.8;" id="ov-body"><strong>Debza Luxury Hotel</strong> stands as a landmark of premium hospitality in <strong>Debre Markos, Ethiopia</strong>. Intended for travelers searching for high-end peace, elite corporate executives visiting the region, and unforgettable family celebrations, Debza Hotel seamlessly balances striking structural architecture with private, secure sanctuary aesthetics. Experience unparalleled premium comfort, exceptional traditional warmth, and elite service standards tailored perfectly to your journey.</p>
    </div>

    <!-- ROOMS & SUITES SECTION -->
    <div id="rooms" class="content-section">
        <img class="section-banner" src="https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=1200" alt="Suites Wing">
        <h2 id="rm-title">Imperial Living Quarters</h2>
        <div class="grid">
            <div class="card">
                <img class="card-img" src="https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500" alt="Sanctuary Suite">
                <h3 id="suite1-title">Executive Sanctuary Suite</h3>
                <p style="color: var(--text-muted);" id="suite1-desc">Configured with 1 King Size Bed, private scenic terraces overlooking Debre Markos, and ambient soft light grids.</p>
                <span class="price"><span id="suite1-price">2,500</span> ETB / <span class="per-night">Night</span></span>
            </div>
            <div class="card">
                <img class="card-img" src="https://images.unsplash.com/photo-1591088398332-8a7791972843?w=500" alt="Imperial Suite">
                <h3 id="suite2-title">Presidential Imperial Suite</h3>
                <p style="color: var(--text-muted);" id="suite2-desc">Comprising 2 Grand Imperial Beds, integrated study chambers, lounge layouts, and secure private corridors.</p>
                <span class="price"><span id="suite2-price">5,000</span> ETB / <span class="per-night">Night</span></span>
            </div>
        </div>
    </div>

    <!-- DINING SECTION -->
    <div id="dining" class="content-section">
        <img class="section-banner" src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200" alt="Dining Lounge">
        <h2 id="din-title">Bespoke Culinary Lounges</h2>
        <div class="grid">
            <div class="card">
                <img class="card-img" src="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=500" alt="Gourmet Menu">
                <h3 id="din-card-title">The Obsidian Room & Grill</h3>
                <p style="color: var(--text-muted);" id="din-card-desc">Michelin-starred fine dining pairing standard Western culinary arts with legendary local flavors and coffee traditions.</p>
            </div>
        </div>
    </div>

    <!-- RESERVATIONS GATEWAY -->
    <div id="booking" class="content-section">
        <div class="form-container">
            <h2 id="form-title">Secure Reservation Console</h2>
            <form action="/process-booking" method="POST">
                <div class="form-group">
                    <label for="name" id="lbl-name">Full Legal Name</label>
                    <input type="text" id="name" name="name" required placeholder="e.g. Abebe Bikila">
                </div>
                <div class="form-group">
                    <label for="phone" id="lbl-phone">Phone Contact</label>
                    <input type="tel" id="phone" name="phone" required placeholder="e.g. 0911234567">
                </div>
                <div class="form-group">
                    <label for="suite" id="lbl-suite">Select Suite Class</label>
                    <select id="suite" name="suite">
                        <option value="Executive Sanctuary Suite" id="opt-s1">Executive Sanctuary Suite (2,500 ETB/N)</option>
                        <option value="Presidential Imperial Suite" id="opt-s2">Presidential Imperial Suite (5,000 ETB/N)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="days" id="lbl-days">Duration of Stay</label>
                    <select id="days" name="days">
                        <option value="1" class="opt-n1">1 Night</option>
                        <option value="2" class="opt-n2">2 Nights</option>
                        <option value="3" class="opt-n3">3 Nights</option>
                        <option value="5" class="opt-n5">5 Nights</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="date" id="lbl-date">Arrival Date</label>
                    <input type="date" id="date" name="date" required>
                </div>
                <button type="submit" class="btn-submit" id="btn-submit">Complete Reservation</button>
            </form>
        </div>
    </div>

    <footer><p>&copy; 2026 Debza Luxury Hotel & Spa. Elite Presentation Portfolio.</p></footer>

    <script>
        let currentLang = 'en';

        const translations = {
            en: {
                tabOverview: "Overview", tabRooms: "Suites", tabDining: "Dining", tabBooking: "Reservations",
                ovTitle: "A Sanctuary of Refinement", ovSubtitle: "Where sovereign luxury meets the rich heritage of Gojjam.",
                ovBody: "<strong>Debza Luxury Hotel</strong> stands as a landmark of premium hospitality in <strong>Debre Markos, Ethiopia</strong>. Intended for travelers searching for high-end peace, elite corporate executives visiting the region, and unforgettable family celebrations, Debza Hotel seamlessly balances striking structural architecture with private, secure sanctuary aesthetics. Experience unparalleled premium comfort, exceptional traditional warmth, and elite service standards tailored perfectly to your journey.",
                rmTitle: "Imperial Living Quarters", suite1Title: "Executive Sanctuary Suite",
                suite1Desc: "Configured with 1 King Size Bed, private scenic terraces overlooking Debre Markos, and ambient soft light grids.",
                suite2Title: "Presidential Imperial Suite",
                suite2Desc: "Comprising 2 Grand Imperial Beds, integrated study chambers, lounge layouts, and secure private corridors.",
                perNight: "Night", dinTitle: "Bespoke Culinary Lounges", dinCardTitle: "The Obsidian Room & Grill",
                dinCardDesc: "Michelin-starred fine dining pairing standard Western culinary arts with legendary local flavors and coffee traditions.",
                formTitle: "Secure Reservation Console", lblName: "Full Legal Name", lblPhone: "Phone Contact",
                lblSuite: "Select Suite Class", lblDays: "Duration of Stay", lblDate: "Arrival Date", btnSubmit: "Complete Reservation",
                optS1: "Executive Sanctuary Suite (2,500 ETB/N)", optS2: "Presidential Imperial Suite (5,000 ETB/N)",
                optN1: "1 Night", optN2: "2 Nights", optN3: "3 Nights", optN5: "5 Nights", toggleText: "አማርኛ"
            },
            am: {
                tabOverview: "አጠቃላይ መግለጫ", tabRooms: "ክፍሎች", tabDining: "ምግብና መጠጥ", tabBooking: "ቦታ ማስያዣ",
                ovTitle: "የምቾት እና የቅንጦት ማረፊያ", ovSubtitle: "የላቀ ዘመናዊ ቅንጦት ከጎጃም ታሪካዊ የእንግዳ ተቀባይነት ባህል ጋር የሚገናኝበት።",
                ovBody: "<strong>ደብዛ ላክዠሪ ሆቴል</strong> በ<strong>ደብረ ማርቆስ፣ ኢትዮጵያ</strong> የላቀ የሆቴል አገልግሎት ተምሳሌት ሆኖ የቆመ ነው። ከፍተኛ ሰላም ለሚፈልጉ ተጓዦች፣ አካባቢውን ለሚጎበኙ የንግድ ባለስልጣናት እና ለማይረሱ የቤተሰብ በዓላት ተመራጭ እንዲሆን ተደርጎ በልዩ ጥበብ የተገነባ ነው። ወደር የሌለው ምቾት፣ ልዩ ባህላዊ መስተንግዶ እና ለእርስዎ የተበጁ ልሂቃን አገልግሎቶችን ያግኙ።",
                rmTitle: "የማዕረግ ስብስቦች", suite1Title: "ኤግዚኪዩቲቭ ሳንክቹዋሪ ስዊት",
                suite1Desc: "1 ባለ ታላቅ (King Size) አልጋ፣ ደብረ ማርቆስን በቁልቁል የሚመለከቱ የግል በረንዳዎች እና ማራኪ የብርሃን ዲዛይን ያለው።",
                suite2Title: "ፕሬዝዳንሻል ኢምፔሪያል ስዊት",
                suite2Desc: "2 ታላላቅ አልጋዎች፣ የስራ ማጥኛ ክፍሎች፣ ዘመናዊ ሳሎን እና አስተማማኝ የግል ኮሪደሮችን ያካተተ ምርጥ ክፍል።",
                perNight: "ሌሊት", dinTitle: "ልዩ የሆኑ የምግብ አዳራሾች", dinCardTitle: "ኦብሰዲያን ሩም እና ግሪል",
                dinCardDesc: "የምዕራባውያን የምግብ አዘገጃጀት ጥበብን ከታዋቂው የሀገር በቀል ጣዕምና የቡና ባህል ጋር ያዋሃደ የቅንጦት ምግብ ቤት።",
                formTitle: "ደህንነቱ የተጠበቀ የቦታ ማስያዣ ማዕከል", lblName: "ሙሉ ህጋዊ ስም", lblPhone: "ስልክ ቁጥር",
                lblSuite: "የክፍል አይነት ይምረጡ", lblDays: "የቆይታ ጊዜ", lblDate: "የመድረሻ ቀን", btnSubmit: "ቦታ ማስያዝ ይጨርሱ",
                optS1: "ኤግዚኪዩቲቭ ሳንክቹዋሪ ስዊት (2,500 ብር/ሌሊት)", optS2: "ፕሬዝዳንሻል ኢምፔሪያል ስዊት (5,000 ብር/ሌሊት)",
                optN1: "1 ሌሊት", optN2: "2 ሌሊት", optN3: "3 ሌሊት", optN5: "5 ሌሊት", toggleText: "English"
            }
        };

        function toggleLanguage() {
            currentLang = (currentLang === 'en') ? 'am' : 'en';
            const data = translations[currentLang];

            // Update Nav Tabs
            document.getElementById('tab-overview').innerText = data.tabOverview;
            document.getElementById('tab-rooms').innerText = data.tabRooms;
            document.getElementById('tab-dining').innerText = data.tabDining;
            document.getElementById('tab-booking').innerText = data.tabBooking;

            // Update Overview
            document.getElementById('ov-title').innerText = data.ovTitle;
            document.getElementById('ov-subtitle').innerText = data.ovSubtitle;
            document.getElementById('ov-body').innerHTML = data.ovBody;

            // Update Rooms
            document.getElementById('rm-title').innerText = data.rmTitle;
            document.getElementById('suite1-title').innerText = data.suite1Title;
            document.getElementById('suite1-desc').innerText = data.suite1Desc;
            document.getElementById('suite2-title').innerText = data.suite2Title;
            document.getElementById('suite2-desc').innerText = data.suite2Desc;
            document.querySelectorAll('.per-night').forEach(el => el.innerText = data.perNight);

            // Update Dining
            document.getElementById('din-title').innerText = data.dinTitle;
            document.getElementById('din-card-title').innerText = data.dinCardTitle;
            document.getElementById('din-card-desc').innerText = data.dinCardDesc;

            // Update Booking Form
            document.getElementById('form-title').innerText = data.formTitle;
            document.getElementById('lbl-name').innerText = data.lblName;
            document.getElementById('lbl-phone').innerText = data.lblPhone;
            document.getElementById('lbl-suite').innerText = data.lblSuite;
            document.getElementById('lbl-days').innerText = data.lblDays;
            document.getElementById('lbl-date').innerText = data.lblDate;
            document.getElementById('btn-submit').innerText = data.btnSubmit;

            // Update Select Options
            document.getElementById('opt-s1').innerText = data.optS1;
            document.getElementById('opt-s2').innerText = data.optS2;
            document.querySelectorAll('.opt-n1').forEach(el => el.innerText = data.optN1);
            document.querySelectorAll('.opt-n2').forEach(el => el.innerText = data.optN2);
            document.querySelectorAll('.opt-n3').forEach(el => el.innerText = data.optN3);
            document.querySelectorAll('.opt-n5').forEach(el => el.innerText = data.optN5);

            // Update Toggle Button Text
            document.getElementById('lang-toggle').innerText = data.toggleText;
        }

        function switchTab(tabId) {
            document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            if(event && event.currentTarget) {
                event.currentTarget.classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process-booking', methods=['POST'])
def process_booking():
    guest_name = request.form.get('name')
    guest_phone = request.form.get('phone')
    selected_suite = request.form.get('suite')
    arrival_date = request.form.get('date')
    total_days = request.form.get('days')
    
    rates = {"Executive Sanctuary Suite": 2500, "Presidential Imperial Suite": 5000}
    base_total = rates.get(selected_suite, 2500) * int(total_days)
    final_amount = base_total * 1.10  

    room_database = {
        "Executive Sanctuary Suite": {"beds": "1 King Size Bed", "floor": "14th Floor"},
        "Presidential Imperial Suite": {"beds": "2 Grand Imperial Beds", "floor": "18th Floor"}
    }
    details = room_database.get(selected_suite)

    report = (
        "👑 *DEBZA LUXURY HOTEL - NEW RESERVATION ALERT* 👑\n"
        "=========================================\n\n"
        "🟢 *STATUS: SUCCESSFUL BOOKING COMPLETED*\n\n"
        "📋 *GUEST PROFILE*\n"
        f"▪️ *Name*: {guest_name}\n"
        f"▪️ *Contact Line*: {guest_phone}\n"
        f"📅 *Check-in Schedule*: {arrival_date} ({total_days} Nights)\n\n"
        "🏨 *ROOM ARCHITECTURAL LAYOUT*\n"
        f"▪️ *Suite Selected*: {selected_suite}\n"
        f"🛏️ *Bed Configuration*: {details['beds']}\n"
        f"🏢 *Assigned Wing*: {details['floor']}\n\n"
        "💰 *FINANCIAL BALANCE*\n"
        f"▪️ *Total Invoice Ledger*: {final_amount:,.2f} ETB\n"
        "=========================================\n"
        "⚡ _System notification triggered. Inventory updated successfully._"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(telegram_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": report, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Telegram Delivery Link Postponed: {e}")

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Reservation Verified</title>
        <style>
            body {{ 
                background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                            url('https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=1600') no-repeat center center fixed;
                background-size: cover;
                color: #FFFFFF; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0;
            }}
            .receipt-card {{ 
                background: rgba(15, 15, 15, 0.95); max-width: 550px; width: 100%; padding: 40px; border-radius: 4px; border: 1px solid #D4AF37; box-shadow: 0 20px 40px rgba(0,0,0,0.9); text-align: center;
            }}
            h1 {{ color: #D4AF37; font-weight: 400; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; font-size: 1.8rem; }}
            p {{ color: #B3B3B3; margin-bottom: 25px; font-size: 1rem; }}
            .folio-details {{ background: rgba(255, 255, 255, 0.02); border-left: 3px solid #D4AF37; padding: 20px; text-align: left; margin-bottom: 25px; }}
            .folio-item {{ margin-bottom: 10px; display: flex; justify-content: space-between; font-size: 0.95rem; }}
            .label {{ color: #B3B3B3; }}
            .value {{ color: #FFFFFF; font-weight: 600; }}
            .btn-back {{ display: inline-block; padding: 12px 30px; background: #D4AF37; color: #0A0A0A; text-decoration: none; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; transition: all 0.3s ease; }}
            .btn-back:hover {{ background: #F3E5AB; box-shadow: 0 0 10px rgba(212,175,55,0.5); }}
        </style>
    </head>
    <body>
        <div class="receipt-card">
            <div style="font-size: 3.5rem; margin-bottom: 15px; color: #D4AF37;">✨</div>
            <h1>Reservation Completed / ቦታ ማስያዝ ተጠናቋል</h1>
            <p>Thank you, {guest_name}. Your reservation requests have been registered into our system logs.</p>
            
            <div class="folio-details">
                <div class="folio-item"><span class="label">Suite Class:</span><span class="value">{selected_suite}</span></div>
                <div class="folio-item"><span class="label">Total Duration:</span><span class="value">{total_days} Nights</span></div>
                <div class="folio-item"><span class="label">Bed Configuration:</span><span class="value">{details['beds']}</span></div>
                <div class="folio-item" style="border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px; margin-top: 10px;"><span class="label" style="color:#D4AF37;">Total Charges:</span><span class="value" style="color:#D4AF37;">{final_amount:,.2f} ETB</span></div>
            </div>
            <a href="/" class="btn-back">Return to Main Terminal</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)