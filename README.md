<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Leafstone — Full Demo</title>
<style>
:root{--accent:#0f766e;--muted:#6b7280;--bg:#f8fafc}
*{box-sizing:border-box;font-family:Inter,system-ui,Segoe UI,Roboto,Arial}
body{margin:0;background:var(--bg);color:#0f172a}
header{background:white;box-shadow:0 1px 3px rgba(2,6,23,.06);position:sticky;top:0;z-index:50}
.container{max-width:1100px;margin:0 auto;padding:16px}
.nav{display:flex;gap:12px;align-items:center}
.brand{font-weight:700;color:var(--accent);font-size:20px}
.search{flex:1}
input,button,select,textarea{font-family:inherit}
input[type=text],input[type=number],input[type=password],select{padding:10px;border:1px solid #e2e2da;border-radius:8px;width:100%}
button{background:var(--accent);color:white;border:0;padding:10px 12px;border-radius:8px;cursor:pointer}
.grid{display:grid;gap:12px}
.hero{background:linear-gradient(90deg,#ecfeff,white);padding:20px;border-radius:10px}
.card{background:white;border-radius:10px;padding:12px;box-shadow:0 1px 2px rgba(2,6,23,.04)}
.product-grid{grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.product img{width:100%;height:160px;object-fit:cover;border-radius:6px;position:relative}
.small{font-size:13px;color:var(--muted)}
.muted{color:var(--muted)}
.flex{display:flex;gap:8px;align-items:center}
footer{padding:20px;text-align:center;color:var(--muted);font-size:14px}
@media(min-width:900px){.container{padding:24px}}
.btn-ghost{background:transparent;color:var(--accent);border:1px solid rgb(220, 215, 208)}
.pill{padding:6px 8px;border-radius:999px;border:1px solid #e6eef2;display:inline-block}
.topbar-actions{display:flex;gap:8px}
.modal{position:fixed;inset:0;background:rgba(3,7,18,.4);display:flex;align-items:center;justify-content:center;padding:20px;z-index:100}
.modal>.card{width:100%;max-width:760px;position:relative}
.closeX{position:absolute;top:8px;right:12px;font-weight:bold;cursor:pointer;font-size:18px;color:var(--muted)}
.product img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 6px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product img:hover {
  transform: scale(1.05);        /* Slight zoom */
  box-shadow: 0 8px 20px rgba(0,0,0,0.2); /* Shadow effect */
  cursor: pointer;               /* Cursor changes on hover */
  .brand .leaf {
  color: red;
  font-weight: 700;
}


.brand .stone {
  color: white;
  font-weight: 700;
}
#btnCart {
  display: flex;
  align-items: center;
  gap: 4px; /* space between icon and count */
  font-size: 16px;
}


}
</style>
</head>
<body>
<header>
  <div class="container nav">
    <div class="brand">
  <span style="color:rgb(210, 12, 12);">Leaf </span><span style="color:rgb(11, 11, 11);">Stone</span>
</div>
    <div class="search">
      <input id="globalSearch" type="text" placeholder="Search products, categories, brands...">
    </div>
    <div class="topbar-actions">
      <button id="btnCategories" class="btn-ghost">Categories</button>
      <button id="btnProfile" class="btn-ghost">Profile</button>
      <button id="btnCart" class="pill">🛒 <span id="cartCount">0</span></button>
      
    </div>
  </div>
</header>
<main class="container" id="app"></main>
<footer>All rights reserved. Your one-stop e-commerce site for browsing and exploring products.© Leafstone</footer>
<div id="modals"></div>


<script>
// --- Sample Products ---
const SAMPLE_PRODUCTS = (() => {
  const cats=['Mobiles','Electronics','Fashion','Home','Books','Toys','Beauty'];
  const imgs=['https://picsum.photos/seed/p1/800/600','https://picsum.photos/seed/p2/800/600','https://picsum.photos/seed/p3/800/600','https://picsum.photos/seed/p4/800/600','https://picsum.photos/seed/p5/800/600','https://picsum.photos/seed/p6/800/600'];
  let list=[];
  for(let i=1;i<=50;i++){
    const category=cats[i%cats.length];
    list.push({id:'P'+(1000+i),title:`${category} Product ${i}`,price:Math.round((50+Math.random()*950)*100)/100,rating:Math.round((3+Math.random()*2)*10)/10,stock:Math.floor(Math.random()*30),category,images:[imgs[i%imgs.length]],desc:`This is a concise description for ${category} Product ${i}.`});
  }
  return list;
})();



// --- LocalStorage helpers ---
function lsGet(k,f){try{const v=localStorage.getItem(k);return v?JSON.parse(v):f}catch(e){return f}}
function lsSet(k,v){localStorage.setItem(k,JSON.stringify(v))}

// --- Initialize ---
if(!lsGet('leaf_products')) lsSet('leaf_products', SAMPLE_PRODUCTS);
if(!lsGet('leaf_orders')) lsSet('leaf_orders',[]);

const state = {
  products: lsGet('leaf_products', SAMPLE_PRODUCTS),
  orders: lsGet('leaf_orders', []),
  currentUser: null,
  cart: lsGet('leaf_cart', []),
  view:{page:'home',params:{}},
  pendingBuy:null
};

function saveAll(){lsSet('leaf_products',state.products); lsSet('leaf_orders',state.orders); lsSet('leaf_cart',state.cart); lsSet('leaf_session',state.currentUser);}

// --- Element helper ---
function el(tag,attrs={},children=[]){const e=document.createElement(tag);for(const k in attrs){if(k.startsWith('on')) e.addEventListener(k.substring(2),attrs[k]);else if(k==='html') e.innerHTML=attrs[k];else e.setAttribute(k,attrs[k]);} (Array.isArray(children)?children:[children]).forEach(c=>{if(typeof c==='string') e.appendChild(document.createTextNode(c));else if(c)e.appendChild(c)});return e}

// --- App ---
const app=document.getElementById('app'), modals=document.getElementById('modals');
state.currentUser = null;
lsSet('leaf_session', null);

function render(){
  document.getElementById('cartCount').textContent=state.cart.reduce((s,i)=>s+i.qty,0);
  app.innerHTML='';
  
  if(state.view.page==='home') renderHome();
  else if(state.view.page==='products') renderProducts();
  else if(state.view.page==='product') renderProductDetail(state.view.params.id);
  else if(state.view.page==='cart') renderCart();
  else if(state.view.page==='checkout') renderCheckout();
  else if(state.view.page==='profile') renderProfile();
}

// --- Home ---
function renderHome(){
  const hero=el('div',{class:'hero card grid'},[
    el('div',{html:'<h2>Welcome to Leafstone</h2><p class="small">"Leafstone is a e-commerce platform designed to showcase products, categories, and shopping functionalities. It allows users to browse items, add them to the cart, and simulate purchases. Built for learning and testing purposes, Leafstone demonstrates the core features of an online store in a simple and interactive way".</p>'}),
    el('div',{class:'flex'},[el('button',{onclick:()=>{state.view.page='products'; state.view.params={}; render()}},'Shop Now')])
  ]);
  const cats=[...new Set(state.products.map(p=>p.category))];
  const categories=el('div',{class:'grid', style:'grid-template-columns:repeat(auto-fit,minmax(120px,1fr));margin-top:12px'}, cats.map(c=>el('div',{class:'card',onclick:()=>{state.view.page='products'; state.view.params={category:c}; render()}}, [el('div',{class:'small'},c), el('div',{html:'&nbsp;'})])));
  const featured=state.products.slice(0,8).map(p=>productCard(p));
  const featuredGrid=el('div',{class:'grid product-grid'},featured);
  app.appendChild(hero); app.appendChild(el('div',{style:'height:12px'}));
  app.appendChild(el('div',{class:'card'},[el('h3',{},'Categories'),categories]));
  app.appendChild(el('div',{style:'height:12px'}));
  app.appendChild(el('div',{class:'card'},[el('h3',{},'Featured Products'),featuredGrid]));
}

// --- Product Card ---
function productCard(p){
  const c = el('div',{class:'card product'},[
    el('img',{
      src: p.images[0],
      alt: p.title,
      onerror: (e) => e.target.src='https://via.placeholder.com/400x300?text=Leafstone',
      onclick: () => {  // <-- add this
        state.view.page = 'product';
        state.view.params = { id: p.id };
        render();
      }
    }),
    el('div',{class:'small'},p.category),
    el('div',{},el('strong',{},p.title)),
    el('div',{class:'flex'},[el('div',{},'₹'+p.price.toFixed(2)), el('div',{class:'small muted'},p.rating+' ★')]),
    el('div',{class:'flex'},[
      el('button',{onclick:()=>{ state.view.page='product'; state.view.params={id:p.id}; render(); }},'View'),
      el('button',{class:'btn-ghost',onclick:()=>{ addToCart(p.id,1); }},'Add')
    ])
  ]);
  return c;
}


// --- Product Detail ---
function renderProductDetail(id){
  const p = state.products.find(x => x.id === id);
  if(!p){ alert('Product not found'); state.view.page='products'; render(); return; }

  app.innerHTML='';

  // Gallery: show all images as thumbnails and main image
  let mainImg = el('img', {
    src: p.images[0],
    style: 'width:100%;height:240px;object-fit:cover;border-radius:8px;margin-bottom:8px'
  });

  // Thumbnails row
  const thumbnails = el('div', {class:'flex', style:'gap:6px'}, 
    p.images.map(src => el('img', {
      src,
      style:'width:60px;height:60px;object-fit:cover;border-radius:4px;cursor:pointer;border:1px solid #e6eef2',
      onclick: (e) => mainImg.src = src // click to change main image
    }))
  );

  const gallery = el('div', {}, [mainImg, thumbnails]);

  const details = el('div', {}, [
    el('h2', {}, p.title),
    el('div', {class:'small'}, p.category + ' • ' + p.rating + ' ★'),
    el('p', {class:'small'}, p.desc),
    el('div', {}, 'Price: ₹' + p.price.toFixed(2)),
    el('div', {style:'height:8px'}),
    el('div', {class:'flex', style:'gap:8px'}, [
      el('button',{onclick:()=>addToCart(p.id,1)},'Add to Cart'),
      el('button',{onclick:()=>{
        if(!state.currentUser){ state.pendingBuy = {id:p.id, qty:1}; state.view.page='profile'; render(); return; }
        state.cart = [{id:p.id, qty:1}]; showPaymentOptions();
      }, style:'background:#f59e0b;color:white;'},'Buy Now'),
      el('button',{class:'btn-ghost', onclick:()=>{state.view.page='products'; render();}},'Back')
    ])
  ]);

  // Render grid: gallery left, details right
  app.appendChild(el('div',{class:'grid', style:'grid-template-columns:1fr 360px;gap:12px'}, [gallery, details]));
}


// --- Profile ---

function saveProfile() {
  const profileData = {
    name: document.getElementById('profile_name').value,
    mobile: document.getElementById('profile_mobile').value,
    addr: document.getElementById('profile_addr').value,
    pincode: document.getElementById('profile_pincode').value
  };

  // Step 1: Create payment popup container
  const paymentPopup = document.createElement('div');
  paymentPopup.style.position = "fixed";
  paymentPopup.style.top = "50%";
  paymentPopup.style.left = "50%";
  paymentPopup.style.transform = "translate(-50%, -50%)";
  paymentPopup.style.background = "#ffffff";
  paymentPopup.style.padding = "30px 40px";
  paymentPopup.style.borderRadius = "16px";
  paymentPopup.style.boxShadow = "0 8px 25px rgba(0, 0, 0, 0.2)";
  paymentPopup.style.zIndex = "9999";
  paymentPopup.style.textAlign = "center";
  paymentPopup.style.fontFamily = "Inter, system-ui, sans-serif";
  paymentPopup.style.transition = "all 0.3s ease";

  paymentPopup.innerHTML = `
    <h2 style="margin-bottom: 15px; color: #0f766e;">Choose Payment Method</h2>

    <div style="display: flex; flex-direction: column; gap: 10px; align-items: flex-start; margin-bottom: 20px;">
      <label style="font-size: 16px; cursor: pointer; color: #333;">
        <input type="radio" name="payment" value="COD" style="margin-right: 8px;"> Cash on Delivery
      </label>
      <label style="font-size: 16px; cursor: pointer; color: #333;">
        <input type="radio" name="payment" value="Online" style="margin-right: 8px;"> Online Payment
      </label>
    </div>

    <button id="confirmOrderBtn" 
      style="
        background: #0f766e; 
        color: white; 
        border: none; 
        padding: 10px 25px; 
        border-radius: 8px; 
        font-size: 16px;
        cursor: pointer;
        transition: background 0.3s ease;
      "
      onmouseover="this.style.background='#0b5e56'" 
      onmouseout="this.style.background='#0f766e'"
    >
      Confirm Order
    </button>
  `;

  document.body.appendChild(paymentPopup);

  // Step 2: Confirm order button click
  document.getElementById("confirmOrderBtn").onclick = function() {
    const selectedPayment = document.querySelector('input[name="payment"]:checked');
    if (!selectedPayment) {
      alert("⚠️ Please select a payment option first!");
      return;
    }

    profileData.payment = selectedPayment.value;
    document.body.removeChild(paymentPopup);

    // Step 3: Send to Google Sheets
    fetch("https://script.google.com/macros/s/AKfycby9iqUnwLtxWuUVs7oINEet7sQUQB7U3ItwKVjy4m69HqCynxZj4G_J3lOsh16pn_hb3g/exec", {
      method: "POST",
      body: JSON.stringify(profileData)
    })
    .then(res => res.text())
    .then(() => {
      // Step 4: Beautiful success popup
      const popup = document.createElement('div');
      popup.innerText = `🎉 Order Confirmed via ${profileData.payment}`;
      popup.style.position = "fixed";
      popup.style.top = "20px";
      popup.style.left = "50%";
      popup.style.transform = "translateX(-50%)";
      popup.style.background = "#0f766e";
      popup.style.color = "white";
      popup.style.padding = "15px 30px";
      popup.style.borderRadius = "12px";
      popup.style.fontSize = "18px";
      popup.style.fontWeight = "600";
      popup.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
      popup.style.zIndex = "9999";
      popup.style.transition = "opacity 0.4s ease";
      document.body.appendChild(popup);

      // Step 5: Remove popup and redirect home
      setTimeout(() => {
        popup.style.opacity = "0";
        setTimeout(() => {
          popup.remove();
          state.view.page = 'home';
          render();
        }, 400);
      }, 2000);
    });
  };
}




function renderProfile(){
  const user = state.currentUser || { name:'', mobile:'', addr:'', pincode:'', email:'', isAdmin:false };

  const profileForm = el('div', { class: 'card', style:'position:relative;' }, [
    el('span', { class:'closeX', onclick:()=>{state.view.page='home'; render();} }, '×'),
    el('h2', {}, 'Your Profile / Create Account'),
    el('input', { id:'profile_name', type:'text', placeholder:'Full Name', value:user.name || '', style:'width:100%;margin-bottom:6px'}),
    el('input', { id:'profile_mobile', type:'text', placeholder:'Mobile', value:user.mobile || '', style:'width:100%;margin-bottom:6px'}),
    el('input', { id:'profile_addr', type:'text', placeholder:'Address', value:user.addr || '', style:'width:100%;margin-bottom:6px'}),
    el('input', { id:'profile_pincode', type:'text', placeholder:'Pincode', value:user.pincode || '', style:'width:100%;margin-bottom:6px'}),
    el('button', { onclick: saveProfile }, 'Save Profile')
  ]);

  app.innerHTML='';
  app.appendChild(profileForm);
}

// --- Cart ---
function addToCart(id,qty){
  const p=state.products.find(x=>x.id===id); if(!p) return alert('Product not found');
  const item=state.cart.find(i=>i.id===id);
  if(item) item.qty+=qty; else state.cart.push({id,qty});
  saveAll(); render(); showToast('Added to cart');
}
function updateCartItem(id,qty){state.cart=state.cart.map(i=>i.id===id?{...i,qty}:i).filter(i=>i.qty>0); saveAll(); render();}
function removeCartItem(id){state.cart=state.cart.filter(i=>i.id!==id); saveAll(); render();}

function renderCart(){
  const rows=state.cart.map(ci=>{
    const p=state.products.find(x=>x.id===ci.id);
    return el('div',{class:'card flex',style:'justify-content:space-between;align-items:center'},[
      el('div',{style:'display:flex;gap:12px;align-items:center'},[el('img',{src:p.images[0],style:'width:80px;height:60px;object-fit:cover;border-radius:6px'}), el('div',{},[el('div',{},p.title), el('div',{class:'small muted'}, '₹'+p.price.toFixed(2))])]),
      el('div',{},[el('input',{type:'number',value:ci.qty,min:1,style:'width:64px',onchange:(e)=>{updateCartItem(ci.id,Number(e.target.value))}}),el('button',{class:'btn-ghost',onclick:()=>removeCartItem(ci.id)},'Remove')])
    ]);
  });
  app.appendChild(el('h2',{},'Your Cart'));
  if(rows.length===0) app.appendChild(el('div',{class:'card'},'Cart is empty.'));
  else {
    rows.forEach(r=>app.appendChild(r));
    const total=state.cart.reduce((s,i)=>{const p=state.products.find(p=>p.id===i.id); return s+(p?p.price*i.qty:0)},0);
    app.appendChild(el('div',{class:'card',style:'text-align:right'},[el('div',{},'Total: ₹'+total.toFixed(2)), el('div',{},el('button',{onclick:()=>{state.view.page='checkout'; render();}},'Proceed to Checkout'))]));
  }
}

// --- Payment modal ---
function showPaymentOptions(){
  if(!state.cart || state.cart.length===0) return alert('Cart is empty');

  let selectedPayment = '';
  const btnStyle = 'flex:1;padding:10px;border-radius:6px;border:1px solid #e6eef2;cursor:pointer;transition:all 0.2s;background:white;color:black;';
  const hoverStyle = 'transform:scale(1.03);opacity:0.9;';

  const codBtn = el('button',{onmouseover:(e)=>e.target.style.cssText+=hoverStyle,onmouseout:(e)=>e.target.style.cssText=btnStyle + (selectedPayment==='COD'?'background:yellow;':''),onclick:()=>{ selectedPayment='COD'; codBtn.style.background='yellow'; onlineBtn.style.background='white'; confirmBtn.disabled=false; }, style: btnStyle}, 'Cash on Delivery');

  const onlineBtn = el('button',{onmouseover:(e)=>e.target.style.cssText+=hoverStyle,onmouseout:(e)=>e.target.style.cssText=btnStyle + (selectedPayment==='Online'?'background:yellow;':''),onclick:()=>{ selectedPayment='Online'; onlineBtn.style.background='yellow'; codBtn.style.background='white'; confirmBtn.disabled=false; }, style: btnStyle}, 'Online Payment');

  const confirmBtn = el('button',{onclick:()=>{ if(!selectedPayment) return alert('Select a payment option first!'); state.paymentMethod = selectedPayment; hideModals(); completeOrder(); }, disabled:true, style:'margin-top:12px;padding:10px;border-radius:6px;background:#0f766e;color:white;border:none;cursor:pointer;width:100%;'}, 'Confirm');

  const m = el('div',{class:'modal'}, el('div',{class:'card'}, [ el('span',{class:'closeX', onclick:hideModals},'×'), el('h3',{},'Select Payment Option'), el('div',{style:'display:flex;gap:12px;margin-top:12px'}, [codBtn, onlineBtn]), el('div',{style:'margin-top:12px'}, confirmBtn) ]));

  modals.innerHTML=''; 
  modals.appendChild(m);
}

// --- Checkout ---
function renderCheckout(){
  const user = state.currentUser;
  if(!user) return alert('Please create profile first!');
  const checkoutCard = el('div',{class:'card', style:'max-width:400px;margin:20px auto;padding:20px;position:relative;'},[
    el('span',{class:'closeX', onclick:()=>{state.view.page='home'; render();}, style:'position:absolute;top:10px;right:12px;cursor:pointer;font-size:18px;color:var(--muted);'},'×'),
    el('h3',{},'Confirm Your Order'),
    el('div',{style:'margin:8px 0'}, 'Total Items: '+state.cart.reduce((s,i)=>s+i.qty,0)),
    el('div',{style:'margin:8px 0'}, 'Total Price: ₹'+state.cart.reduce((s,i)=>{ const p=state.products.find(x=>x.id===i.id); return s+(p?p.price*i.qty:0); },0).toFixed(2)),
    el('button',{onclick:showPaymentOptions},'Choose Payment')
  ]);
  app.innerHTML=''; app.appendChild(checkoutCard);
}

// --- Complete order (logs to console only) ---
function completeOrder(){
  const user = state.currentUser;
  if(!user) return alert('Please create profile first!');
  if(!state.paymentMethod) return alert('Select a payment option first!');

  const orderId='ORD'+Date.now();
  const items=state.cart.map(i=>({...i,price:state.products.find(p=>p.id===i.id).price}));
  const order={
    id:orderId,
    user:user.email||'guest@leafstone.test',
    name:user.name,
    email:user.email||'guest@leafstone.test',
    mobile:user.mobile,
    addr:user.addr,
    items,
    status:'Processing',
    deliveryDate:'',
    paymentMethod:state.paymentMethod,
    date:new Date().toISOString()
  };

  state.orders.push(order);
  state.cart=[];
  state.paymentMethod=''; // reset
  saveAll();

  console.log("New Order Placed:", order); // ← Only in console

  alert('Order Placed! Thank you '+user.name);
  state.view.page='home';
  render();
}

// --- Modals ---
function hideModals(){modals.innerHTML='';}
function showToast(msg){alert(msg);}

// --- Navigation ---
document.getElementById('btnProfile').onclick=()=>{ state.view.page='profile'; render(); }
document.getElementById('btnCart').onclick=()=>{ state.view.page='cart'; render(); }
document.getElementById('btnCategories').onclick=()=>{ state.view.page='products'; state.view.params={}; render(); }

function renderProducts(){
  const cat = state.view.params.category;
  const filtered = cat?state.products.filter(p=>p.category===cat):state.products;
  app.innerHTML = '';
  if(cat) app.appendChild(el('h2',{},'Category: '+cat));
  const grid=el('div',{class:'grid product-grid'}, filtered.map(productCard));
  app.appendChild(grid);
}

// --- Initial render ---
render();
const searchInput = document.getElementById('globalSearch');
const placeholderTexts = [
  "Search products...",
  "Search categories...",
  "Search brands...",
  "Find electronics...",
  "Discover fashion..."
];

let placeholderIndex = 0;

function rotatePlaceholder() {
  searchInput.setAttribute('placeholder', placeholderTexts[placeholderIndex]);
  placeholderIndex = (placeholderIndex + 1) % placeholderTexts.length;
}

// Change placeholder every 2 seconds (2000 ms)
setInterval(rotatePlaceholder, 2000);
// --- Search Handler ---
searchInput.addEventListener('keypress', function(e){
    if(e.key === 'Enter'){
        const query = searchInput.value.trim().toLowerCase();
        if(!query) return;

        // First try exact match on product title
        const exactMatch = state.products.find(p => p.title.toLowerCase() === query);

        if(exactMatch){
            // Redirect to product detail
            state.view.page = 'product';
            state.view.params = { id: exactMatch.id };
            render();
            return;
        }

        // Partial match: title or category contains query
        const similarProducts = state.products.filter(p => 
            p.title.toLowerCase().includes(query) || p.category.toLowerCase().includes(query)
        );

        if(similarProducts.length){
            state.view.page = 'products';
            state.view.params = {};
            app.innerHTML = '';
            app.appendChild(el('h2',{},`Search Results for "${query}"`));
            const grid = el('div',{class:'grid product-grid'}, similarProducts.map(productCard));
            app.appendChild(grid);
        } else {
            alert('No products found matching "' + query + '"');
        }
    }
});

  fetch('http://127.0.0.1:5000/orders')
    .then(res => res.json())
    .then(data => console.log(data)) // prints orders in browser console
    .catch(err => console.error('Error fetching orders:', err));


</script>
</body>
</html>
