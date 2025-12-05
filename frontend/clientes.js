const API_URL = "http://localhost:8500/api/clients/";
const ORDERS_API = "http://localhost:8500/api/clients/";

document.addEventListener("DOMContentLoaded", loadClients);


// =====================================================
// CREAR / EDITAR CLIENTE
// =====================================================

document.getElementById("client-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = document.getElementById("client-id").value;
    const data = {
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        email: document.getElementById("email").value
    };

    if (id) await updateClient(id, data);
    else await createClient(data);

    await loadClients();
    resetForm();
});


// =====================================================
// CARGAR CLIENTES
// =====================================================

async function loadClients() {
    const res = await fetch(API_URL);
    const data = await res.json();

    const tbody = document.getElementById("clients-body");
    tbody.innerHTML = "";

    (data.results || []).forEach(c => {
        tbody.innerHTML += `
            <tr>
                <td>${c.name}</td>
                <td>${c.phone}</td>
                <td>${c.email}</td>
                <td>
                    <button class="action-btn edit-btn" onclick="editClient(${c.id}, '${c.name}', '${c.phone}', '${c.email}')">Editar</button>
                    <button class="action-btn delete-btn" onclick="deleteClient(${c.id})">Eliminar</button>
                    <button class="action-btn" onclick="getOrders(${c.id})">Órdenes</button>
                </td>
            </tr>
        `;
    });
}


// CRUD cliente

async function createClient(data) {
    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

function editClient(id, name, phone, email) {
    document.getElementById("client-id").value = id;
    document.getElementById("name").value = name;
    document.getElementById("phone").value = phone;
    document.getElementById("email").value = email;

    document.getElementById("form-title").innerText = "Editar Cliente";
    document.getElementById("cancel-edit").style.display = "block";
}

async function updateClient(id, data) {
    await fetch(`${API_URL}${id}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

async function deleteClient(id) {
    if (!confirm("¿Eliminar cliente?")) return;

    await fetch(`${API_URL}${id}/`, {
        method: "DELETE"
    });

    loadClients();
}


// CONSULTAR ÓRDENES DEL CLIENTE

async function getOrders(id) {
    const res = await fetch(`${ORDERS_API}${id}/orders/`);
    const orders = await res.json();

    const container = document.getElementById("orders-list");
    container.innerHTML = "";

    if (orders.length === 0) {
        container.innerHTML = "<li>No tiene órdenes registradas.</li>";
        return;
    }

    orders.forEach(o => {
        container.innerHTML += `
            <li class="orders-item">
                <strong>Código:</strong> ${o.code} <br>
                <strong>Auto:</strong> ${o.car} <br>
                <strong>Servicio:</strong> ${o.servicio} <br>
                <strong>Entrega:</strong> ${o.delivery_Date}
            </li>
        `;
    });
}


// RESETEAR FORMULARIO

document.getElementById("cancel-edit").addEventListener("click", resetForm);

function resetForm() {
    document.getElementById("client-id").value = "";
    document.getElementById("client-form").reset();
    document.getElementById("form-title").innerText = "Crear Cliente";
    document.getElementById("cancel-edit").style.display = "none";
}
