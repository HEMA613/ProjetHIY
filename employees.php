<?php
include 'data.php';
$employees = load_employees();

// Ajouter un employé
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['add_employee'])) {
    $new_employee = [
        'id' => max(array_column($employees, 'id')) + 1,
        'name' => $_POST['name']
    ];
    $employees[] = $new_employee;
    save_employees($employees);
    header('Location: employees.php');
    exit;
}

// Supprimer un employé
if (isset($_GET['delete'])) {
    $id = $_GET['delete'];
    $employees = array_filter($employees, function($e) use ($id) { return $e['id'] != $id; });
    save_employees($employees);
    header('Location: employees.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestion des Employés - HIY</title>
    <link rel="stylesheet" href="index.css">
</head>
<body>
    <header>
        <h1>Système de Gestion des Congés - HIY</h1>
        <nav>
            <a href="index.php">Accueil</a>
            <a href="employees.php">Employés</a>
            <a href="vacations.php">Demandes de Congé</a>
            <a href="calendar.php">Calendrier</a>
        </nav>
    </header>
    <main>
        <section>
            <h2>Gestion des Employés</h2>
            <form method="post">
                <label for="name">Nom de l'Employé:</label>
                <input type="text" id="name" name="name" required>
                <button type="submit" name="add_employee">Ajouter Employé</button>
            </form>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nom</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($employees as $employee): ?>
                    <tr>
                        <td><?php echo $employee['id']; ?></td>
                        <td><?php echo $employee['name']; ?></td>
                        <td><a href="?delete=<?php echo $employee['id']; ?>" onclick="return confirm('Supprimer cet employé ?')">Supprimer</a></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </section>
    </main>
    <footer>
        <p>&copy; 2024 HIY - Système de Gestion des Congés</p>
    </footer>
</body>
</html>