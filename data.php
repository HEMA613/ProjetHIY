<?php
// data.php - Gestion des données

$employees_file = 'employees.json';
$vacations_file = 'vacations.json';

// Charger les employés
function load_employees() {
    global $employees_file;
    if (file_exists($employees_file)) {
        return json_decode(file_get_contents($employees_file), true);
    }
    // Employés par défaut
    return [
        ['id' => 1, 'name' => 'Alice Dupont'],
        ['id' => 2, 'name' => 'Bob Martin'],
        ['id' => 3, 'name' => 'Claire Bernard'],
        ['id' => 4, 'name' => 'David Petit'],
        ['id' => 5, 'name' => 'Emma Moreau'],
        ['id' => 6, 'name' => 'François Durand'],
        ['id' => 7, 'name' => 'Gabrielle Leroy'],
        ['id' => 8, 'name' => 'Henri Simon'],
        ['id' => 9, 'name' => 'Isabelle Michel'],
        ['id' => 10, 'name' => 'Jean Lefebvre']
    ];
}

// Sauvegarder les employés
function save_employees($employees) {
    global $employees_file;
    file_put_contents($employees_file, json_encode($employees, JSON_PRETTY_PRINT));
}

// Charger les congés
function load_vacations() {
    global $vacations_file;
    if (file_exists($vacations_file)) {
        return json_decode(file_get_contents($vacations_file), true);
    }
    return [];
}

// Sauvegarder les congés
function save_vacations($vacations) {
    global $vacations_file;
    file_put_contents($vacations_file, json_encode($vacations, JSON_PRETTY_PRINT));
}
?>