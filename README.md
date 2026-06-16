@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:'Inter',sans-serif;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    overflow:hidden;

    background:#020617;
    position:relative;
}

/* Animated Background */

body::before{
    content:'';
    position:absolute;
    width:700px;
    height:700px;
    background:#2563eb;
    border-radius:50%;
    filter:blur(180px);
    top:-200px;
    left:-200px;
    opacity:0.35;
    animation:float1 8s ease-in-out infinite;
}

body::after{
    content:'';
    position:absolute;
    width:700px;
    height:700px;
    background:#06b6d4;
    border-radius:50%;
    filter:blur(180px);
    bottom:-250px;
    right:-250px;
    opacity:0.25;
    animation:float2 10s ease-in-out infinite;
}

@keyframes float1{
    50%{
        transform:translateY(40px);
    }
}

@keyframes float2{
    50%{
        transform:translateY(-40px);
    }
}

/* Main Container */

.box{
    position:relative;
    z-index:5;

    width:100%;
    max-width:850px;

    padding:40px;

    background:rgba(15,23,42,.65);

    backdrop-filter:blur(20px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:28px;

    box-shadow:
        0 0 60px rgba(37,99,235,.15),
        0 30px 80px rgba(0,0,0,.5);
}

/* Title */

h2{
    text-align:center;
    font-size:42px;
    font-weight:800;

    background:linear-gradient(
        90deg,
        #38bdf8,
        #60a5fa,
        #22d3ee
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    margin-bottom:15px;
}

.subtitle{
    text-align:center;
    color:#94a3b8;
    margin-bottom:30px;
}

/* Labels */

label{
    display:block;
    margin-top:20px;
    margin-bottom:10px;

    color:#e2e8f0;
    font-weight:600;
}

/* Inputs */

input{
    width:100%;

    padding:16px;

    border-radius:16px;

    background:#0f172a;

    border:1px solid rgba(255,255,255,.08);

    color:white;

    outline:none;

    transition:.3s;
}

input:focus{
    border-color:#38bdf8;

    box-shadow:
        0 0 20px rgba(56,189,248,.3);
}

/* Buttons */

.load-btn,
.ask-btn{

    width:100%;

    margin-top:18px;

    border:none;

    padding:16px;

    border-radius:16px;

    font-size:16px;

    font-weight:700;

    cursor:pointer;

    transition:.3s;
}

.load-btn{

    background:linear-gradient(
        135deg,
        #2563eb,
        #3b82f6
    );

    color:white;
}

.ask-btn{

    background:linear-gradient(
        135deg,
        #10b981,
        #22c55e
    );

    color:white;
}

.load-btn:hover,
.ask-btn:hover{

    transform:translateY(-4px);

    box-shadow:
        0 10px 30px rgba(37,99,235,.4);
}

/* Response */

.response-box{

    margin-top:30px;

    background:#0f172a;

    border-radius:20px;

    padding:25px;

    border:1px solid rgba(255,255,255,.06);

    min-height:180px;

    position:relative;
}

.response-box::before{

    content:'AI RESPONSE';

    position:absolute;

    top:-12px;
    left:20px;

    background:#020617;

    color:#38bdf8;

    padding:0 10px;

    font-size:12px;

    letter-spacing:2px;
}

.response-box strong{
    color:#38bdf8;
}

.response-box p{

    margin-top:15px;

    color:#e2e8f0;

    line-height:1.8;
}

/* Mobile */

@media(max-width:768px){

    .box{
        padding:25px;
    }

    h2{
        font-size:32px;
    }
}