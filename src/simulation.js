const API_BASE = "https://5zkbyoqs9e.execute-api.us-east-1.amazonaws.com/prod/products";

// Load products from DynamoDB
async function loadProducts() {
  const table = document.getElementById("productRows");
  table.innerHTML = "";
  const res = await fetch(API_BASE);
  const products = await res.json();

  products.forEach((p) => {
    const row = document.createElement("tr");
    row.dataset.id = p.product_id;
    row.innerHTML = `
      <td contenteditable="true">${p.name}</td>
      <td contenteditable="true">${p.price}</td>
      <td contenteditable="true">${p.inventory ?? p.stock}</td>
      <td>
        <button class="saveBtn">Save</button>
        <button class="deleteBtn">Delete</button>
      </td>
    `;
    table.appendChild(row);
  });

  document.querySelectorAll(".saveBtn").forEach(btn =>
    btn.onclick = e => saveProduct(e.target.closest("tr"))
  );
  document.querySelectorAll(".deleteBtn").forEach(btn =>
    btn.onclick = e => deleteProduct(e.target.closest("tr"))
  );
}

// Add new product
async function addProduct() {
  const name = document.getElementById("newName").value;
  const price = parseFloat(document.getElementById("newPrice").value);
  const stock = parseInt(document.getElementById("newStock").value);
  if (!name || isNaN(price) || isNaN(stock)) return alert("Fill all fields!");

  const newItem = {
    product_id: name.toLowerCase().replace(/\s+/g, "_"),
    name,
    price,
    inventory: stock
  };

  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action: "add", item: newItem })
  });

  alert("Product added!");
  loadProducts();
}

// Save updated product
async function saveProduct(row) {
  const updatedItem = {
    product_id: row.dataset.id,
    name: row.children[0].innerText,
    price: parseFloat(row.children[1].innerText),
    inventory: parseInt(row.children[2].innerText)
  };

  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action: "update", item: updatedItem })
  });

  alert("Product updated!");
}

// Delete product
async function deleteProduct(row) {
  const id = row.dataset.id;
  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action: "delete", item: { product_id: id } })
  });

  row.remove();
  alert("Product deleted!");
}

document.getElementById("addProductBtn").addEventListener("click", addProduct);
window.onload = loadProducts;
