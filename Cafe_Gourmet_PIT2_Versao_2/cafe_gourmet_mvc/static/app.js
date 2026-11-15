let products = [], cart = {}, cat = "Todos", adminLogged = false, adminOrders = [];
const $ = id => document.getElementById(id);
const money = n => Number(n).toLocaleString("pt-BR", {style:"currency", currency:"BRL"});
async function api(url, opts = {}) {
  const response = await fetch(url, {headers:{"Content-Type":"application/json"}, ...opts});
  const data = await response.json();
  if (!response.ok) throw Error(data.error || "Não foi possível concluir a operação.");
  return data;
}
function safe(value) { return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function safeImage(url) { return /^https?:\/\//i.test(url || "") ? safe(url) : ""; }
async function loadProducts() { products = await api("/api/products"); renderFeatured(); renderMenu(); }
function count() { $("count").textContent = Object.values(cart).reduce((a,b) => a+b, 0); }
function view(name) {
  document.querySelectorAll(".panel").forEach(panel => panel.classList.remove("on"));
  $(name).classList.add("on"); $("hero").style.display = name === "home" ? "block" : "none";
  document.querySelectorAll("nav button").forEach(button => button.classList.toggle("active", button.dataset.v === name));
  if (name === "menu") renderMenu(); if (name === "cart") renderCart(); if (name === "admin") refreshAdmin();
  scrollTo({top:0, behavior:"smooth"});
}
document.querySelectorAll("nav button").forEach(button => button.onclick = () => view(button.dataset.v));
function card(product) {
  const picture = safeImage(product.image_url);
  return `<article class="product"><div class="pic">${picture ? `<img src="${picture}" alt="${safe(product.name)}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='grid'">` : ""}<span class="emoji-fallback" style="${picture ? "display:none" : ""}">${safe(product.emoji || "☕")}</span><span class="tag">${safe(product.category)}</span></div><div class="body"><h3>${safe(product.name)}</h3><p>${safe(product.description)}</p><div class="bottom"><span class="price">${money(product.price)}</span><button class="add" onclick="add(${product.id})">Adicionar +</button></div></div></article>`;
}
function renderFeatured() { $("featured").innerHTML = products.filter(p => p.active && p.featured).map(card).join(""); }
function renderMenu() {
  const categories = ["Todos", ...new Set(products.map(p => p.category))];
  $("filters").innerHTML = categories.map(c => `<button class="${cat===c?"sel":""}" onclick="setCat('${safe(c)}')">${safe(c)}</button>`).join("");
  const query = ($("search").value || "").toLowerCase();
  const filtered = products.filter(p => p.active && (cat === "Todos" || p.category === cat) && (p.name.toLowerCase().includes(query) || (p.description || "").toLowerCase().includes(query)));
  $("list").innerHTML = filtered.length ? filtered.map(card).join("") : '<div class="empty">Nenhum produto encontrado.</div>';
}
function setCat(category) { cat = category; renderMenu(); }
function add(id) { cart[id] = (cart[id] || 0) + 1; count(); renderCart(); }
function renderCart() {
  const items = Object.entries(cart).filter(([id, qty]) => qty > 0 && products.some(p => p.id == id));
  let subtotal = 0;
  $("items").innerHTML = items.length ? items.map(([id, qty]) => {
    const p = products.find(product => product.id == id); subtotal += p.price * qty;
    return `<div class="row cart-row"><div><b>${safe(p.name)}</b><br><small>${money(p.price)} cada</small></div><div class="qty"><button aria-label="Diminuir quantidade" onclick="qty(${id},-1)">−</button><b>${qty}</b><button aria-label="Aumentar quantidade" onclick="qty(${id},1)">+</button><strong>${money(p.price*qty)}</strong></div></div>`;
  }).join("") : '<div class="empty">Seu carrinho está vazio.</div>';
  const fee = subtotal ? 5 : 0;
  $("summaryItems").innerHTML = items.length ? items.map(([id, qty]) => { const p=products.find(x=>x.id==id); return `<div class="summary-line"><span>${qty}x ${safe(p.name)}</span><b>${money(p.price*qty)}</b></div>`; }).join("") : '<small>Adicione produtos para visualizar o resumo.</small>';
  $("sub").textContent = money(subtotal); $("fee").textContent = money(fee); $("total").textContent = money(subtotal+fee);
}
function qty(id, amount) { cart[id] = (cart[id] || 0) + amount; if (cart[id] <= 0) delete cart[id]; count(); renderCart(); }
async function checkout() {
  const message = $("msg");
  const items = Object.entries(cart).filter(([id,qty])=>qty>0).map(([id,qty])=>({product_id:Number(id),quantity:qty}));
  if (!items.length) { message.innerHTML = '<div class="notice error">Adicione pelo menos um produto ao carrinho.</div>'; return; }
  try {
    const result = await api("/api/orders", {method:"POST", body:JSON.stringify({name:$("name").value, phone:$("phone").value, address:$("address").value, note:$("note").value, items})});
    const orderId = result.id; const phone = $("phone").value;
    cart = {}; count(); renderCart();
    ["name","phone","address","note"].forEach(id => $(id).value = "");
    message.innerHTML = `<div class="confirmation"><div class="confirm-icon">✓</div><h3>Pedido confirmado!</h3><p>Seu pedido foi registrado com sucesso.</p><div class="order-number">Pedido #${orderId}</div><p>Guarde esse número. Para acompanhar a situação, acesse <b>Acompanhar pedido</b> e informe o número e o telefone utilizado.</p><button class="primary" onclick="view('orders');$('trackId').value='${orderId}'">Acompanhar pedido</button></div>`;
  } catch (error) { message.innerHTML = `<div class="notice error">${safe(error.message)}</div>`; }
}
async function trackOrder() {
  const target = $("trackingResult"); const id = Number($("trackId").value); const phone = $("trackPhone").value.trim();
  if (!id || !phone) { target.innerHTML = '<div class="notice error">Informe o número do pedido e o telefone.</div>'; return; }
  try {
    const order = await api(`/api/orders/${id}/tracking?phone=${encodeURIComponent(phone)}`);
    target.innerHTML = `<div class="tracking-card"><div class="tracking-top"><b>Pedido #${order.id}</b><span class="status">${safe(order.status)}</span></div><p>Data: ${safe(order.created_at)}</p><div class="tracking-items">${order.items.map(item=>`<div>${item.quantity}x ${safe(item.product_name)} <b>${money(item.unit_price*item.quantity)}</b></div>`).join("")}</div><div class="line"><span>Subtotal</span><b>${money(order.subtotal)}</b></div><div class="line"><span>Entrega</span><b>${money(order.delivery_fee)}</b></div><div class="line grand"><span>Total</span><b>${money(order.total)}</b></div></div>`;
  } catch (error) { target.innerHTML = `<div class="notice error">${safe(error.message)}</div>`; }
}
async function loginAdmin() {
  const message = $("loginMsg");
  try { await api("/api/login", {method:"POST", body:JSON.stringify({username:$("loginUser").value, password:$("loginPass").value})}); adminLogged=true; $("loginPass").value=""; await refreshAdmin(); }
  catch(error) { message.innerHTML = `<div class="notice error">${safe(error.message)}</div>`; }
}
async function logoutAdmin() { try { await api("/api/logout", {method:"POST"}); adminLogged=false; await refreshAdmin(); } catch(error) { alert(error.message); } }
async function refreshAdmin() {
  try { const status = await api("/api/session"); adminLogged = status.logged_in; }
  catch { adminLogged = false; }
  $("loginBox").hidden = adminLogged; $("adminContent").hidden = !adminLogged;
  if (adminLogged) { try { await loadProducts(); adminOrders = await api("/api/orders"); renderAdmin(); } catch(error) { alert(error.message); } }
}
async function addProduct() {
  const message = $("adminmsg");
  try {
    await api("/api/products", {method:"POST", body:JSON.stringify({name:$("pname").value, category:$("pcat").value, price:$("pprice").value, emoji:$("pemoji").value, description:$("pdesc").value, image_url:$("pimage").value})});
    ["pname","pprice","pemoji","pdesc","pimage"].forEach(id=>$(id).value="");
    message.innerHTML='<div class="notice">Produto cadastrado com sucesso.</div>'; await loadProducts();
  } catch(error) { message.innerHTML=`<div class="notice error">${safe(error.message)}</div>`; }
}
async function toggleProduct(id, active) { try { await api(`/api/products/${id}`, {method:"PATCH",body:JSON.stringify({active:!active})}); await loadProducts(); renderAdmin(); } catch(error) { alert(error.message); } }
async function deleteProduct(id) { if (!confirm("Excluir este produto?")) return; try { await api(`/api/products/${id}`,{method:"DELETE"}); await loadProducts(); renderAdmin(); } catch(error) { alert(error.message); } }
async function changeStatus(id, status) { try { await api(`/api/orders/${id}`,{method:"PATCH",body:JSON.stringify({status})}); adminOrders=await api("/api/orders"); renderAdmin(); } catch(error) { alert(error.message); } }
function renderAdmin() {
  $("ptable").innerHTML = products.map(p=>`<tr><td><div class="admin-product">${p.image_url?`<img src="${safeImage(p.image_url)}" alt="">`:`<span>${safe(p.emoji)}</span>`}<b>${safe(p.name)}</b></div></td><td>${safe(p.category)}</td><td>${money(p.price)}</td><td>${p.active?"Disponível":"Indisponível"}</td><td><button class="small" onclick="toggleProduct(${p.id},${!!p.active})">${p.active?"Desativar":"Ativar"}</button> <button class="small danger" onclick="deleteProduct(${p.id})">Excluir</button></td></tr>`).join("");
  const query = ($("orderSearch").value || "").toLowerCase();
  const filtered = adminOrders.filter(o=>String(o.id).includes(query)||o.customer_name.toLowerCase().includes(query)||o.status.toLowerCase().includes(query));
  $("adminorders").innerHTML = filtered.length ? filtered.map(o=>`<div class="row admin-order"><div><b>Pedido #${o.id} · ${safe(o.customer_name)}</b><br><small>${safe(o.phone)} · ${o.items.map(i=>i.quantity+"x "+safe(i.product_name)).join(", ")} · ${money(o.total)}</small><br><small>${safe(o.created_at)}</small></div><select aria-label="Status do pedido ${o.id}" onchange="changeStatus(${o.id},this.value)">${["Recebido","Em preparo","Pronto para retirada","Saiu para entrega","Concluído","Cancelado"].map(s=>`<option ${o.status===s?"selected":""}>${s}</option>`).join("")}</select></div>`).join("") : '<div class="empty">Nenhum pedido encontrado.</div>';
}
(async()=>{try{await loadProducts();count();}catch(error){alert("Erro ao conectar com o servidor: "+error.message);}})();
