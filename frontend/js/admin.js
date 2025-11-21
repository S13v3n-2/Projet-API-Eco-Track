// Gestion de l'administration
const admin = {
    currentUsers: [],
    editingUserId: null,

    // Charger tous les utilisateurs
    loadUsers: async function() {
        document.getElementById('users-loading').style.display = 'block';
        document.getElementById('users-list').innerHTML = '';

        try {
            const response = await App.apiRequest(`${App.API_BASE}/admin/users/`);

            if (response.ok) {
                this.currentUsers = await response.json();
                this.displayUsers(this.currentUsers);
            } else if (response.status === 403) {
                App.showMessage('Accès refusé - Droits administrateur requis', 'error');
            } else {
                App.showMessage('Erreur lors du chargement des utilisateurs', 'error');
            }
        } catch (error) {
            console.error('Error loading users:', error);
            App.showMessage('Erreur lors du chargement des utilisateurs', 'error');
        } finally {
            document.getElementById('users-loading').style.display = 'none';
        }
    },

    // Afficher la liste des utilisateurs
    displayUsers: function(users) {
        const usersList = document.getElementById('users-list');

        if (users.length === 0) {
            usersList.innerHTML = '<div class="loading">Aucun utilisateur trouvé</div>';
            return;
        }

        usersList.innerHTML = users.map(user => `
            <div class="user-card ${user.is_active ? '' : 'user-inactive'}">
                <div class="user-header">
                    <div class="user-name">${user.full_name}</div>
                    <div class="user-badges">
                        ${user.role === 'admin' ? '<span class="badge badge-admin">ADMIN</span>' : '<span class="badge badge-user">USER</span>'}
                        ${user.is_active ? '<span class="badge badge-active">ACTIF</span>' : '<span class="badge badge-inactive">INACTIF</span>'}
                    </div>
                </div>
                <div class="user-email">📧 ${user.email}</div>
                <div class="user-id">🆔 ID: ${user.id}</div>
                <div class="user-actions">
                    <button class="btn btn-sm btn-warning" onclick="admin.showEditUserForm(${user.id})">✏️ Modifier</button>
                    ${user.id !== App.currentUser.id ? `<button class="btn btn-sm btn-danger" onclick="admin.deleteUser(${user.id})">🗑️ Supprimer</button>` : ''}
                </div>
                
                <!-- Formulaire d'édition -->
                <div id="edit-form-${user.id}" class="edit-user-form" style="display: none;">
                    <h4>Modifier l'utilisateur</h4>
                    <div class="form-group">
                        <label>Nom complet:</label>
                        <input type="text" id="edit-name-${user.id}" value="${user.full_name}">
                    </div>
                    <div class="form-group">
                        <label>Email:</label>
                        <input type="email" id="edit-email-${user.id}" value="${user.email}">
                    </div>
                    <div class="form-group">
                        <label>Rôle:</label>
                        <select id="edit-role-${user.id}">
                            <option value="user" ${user.role === 'user' ? 'selected' : ''}>Utilisateur</option>
                            <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Administrateur</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Statut:</label>
                        <select id="edit-active-${user.id}">
                            <option value="true" ${user.is_active ? 'selected' : ''}>Actif</option>
                            <option value="false" ${!user.is_active ? 'selected' : ''}>Inactif</option>
                        </select>
                    </div>
                    <button class="btn btn-success" onclick="admin.updateUser(${user.id})">💾 Sauvegarder</button>
                    <button class="btn btn-warning" onclick="admin.hideEditUserForm(${user.id})">❌ Annuler</button>
                </div>
            </div>
        `).join('');
    },

    // Afficher le formulaire de création
    showCreateUserForm: function() {
        document.getElementById('create-user-form').style.display = 'block';
        // Réinitialiser les champs
        document.getElementById('new-user-name').value = '';
        document.getElementById('new-user-email').value = '';
        document.getElementById('new-user-password').value = '';
        document.getElementById('new-user-role').value = 'user';
        document.getElementById('new-user-active').value = 'true';
    },

    // Cacher le formulaire de création
    hideCreateUserForm: function() {
        document.getElementById('create-user-form').style.display = 'none';
    },

    // Créer un nouvel utilisateur
    createUser: async function() {
        const userData = {
            full_name: document.getElementById('new-user-name').value,
            email: document.getElementById('new-user-email').value,
            password: document.getElementById('new-user-password').value,
            role: document.getElementById('new-user-role').value,
            is_active: document.getElementById('new-user-active').value === 'true'
        };

        if (!userData.full_name || !userData.email || !userData.password) {
            App.showMessage('Veuillez remplir tous les champs obligatoires', 'error');
            return;
        }

        try {
            const response = await App.apiRequest(`${App.API_BASE}/auth/register`, {
                method: 'POST',
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                App.showMessage('Utilisateur créé avec succès', 'success');
                this.hideCreateUserForm();
                this.loadUsers(); // Recharger la liste
            } else {
                const error = await response.json();
                App.showMessage(error.detail || 'Erreur lors de la création', 'error');
            }
        } catch (error) {
            console.error('Error creating user:', error);
            App.showMessage('Erreur lors de la création de l\'utilisateur', 'error');
        }
    },

    // Afficher le formulaire d'édition
    showEditUserForm: function(userId) {
        // Cacher tous les autres formulaires d'édition
        document.querySelectorAll('.edit-user-form').forEach(form => {
            form.style.display = 'none';
        });
        document.getElementById(`edit-form-${userId}`).style.display = 'block';
        this.editingUserId = userId;
    },

    // Cacher le formulaire d'édition
    hideEditUserForm: function(userId) {
        document.getElementById(`edit-form-${userId}`).style.display = 'none';
        this.editingUserId = null;
    },

    // Mettre à jour un utilisateur
    updateUser: async function(userId) {
        const userData = {
            full_name: document.getElementById(`edit-name-${userId}`).value,
            email: document.getElementById(`edit-email-${userId}`).value,
            role: document.getElementById(`edit-role-${userId}`).value,
            is_active: document.getElementById(`edit-active-${userId}`).value === 'true'
        };

        try {
            const response = await App.apiRequest(`${App.API_BASE}/admin/users/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                App.showMessage('Utilisateur mis à jour avec succès', 'success');
                this.hideEditUserForm(userId);
                this.loadUsers(); // Recharger la liste
            } else {
                const error = await response.json();
                App.showMessage(error.detail || 'Erreur lors de la mise à jour', 'error');
            }
        } catch (error) {
            console.error('Error updating user:', error);
            App.showMessage('Erreur lors de la mise à jour de l\'utilisateur', 'error');
        }
    },

    // Supprimer un utilisateur
    deleteUser: async function(userId) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ? Cette action est irréversible.')) {
            return;
        }

        try {
            const response = await App.apiRequest(`${App.API_BASE}/admin/users/${userId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                App.showMessage('Utilisateur supprimé avec succès', 'success');
                this.loadUsers(); // Recharger la liste
            } else {
                const error = await response.json();
                App.showMessage(error.detail || 'Erreur lors de la suppression', 'error');
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            App.showMessage('Erreur lors de la suppression de l\'utilisateur', 'error');
        }
    }
};