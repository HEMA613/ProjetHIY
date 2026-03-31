<?php
include 'data.php';
$employees = load_employees();
$vacations = load_vacations();

// Demander un congé
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['request_vacation'])) {
    $new_vacation = [
        'id' => count($vacations) + 1,
        'employee_id' => $_POST['employee_id'],
        'start_date' => $_POST['start_date'],
        'end_date' => $_POST['end_date'],
        'reason' => $_POST['reason'],
        'status' => 'pending'
    ];
    $vacations[] = $new_vacation;
    save_vacations($vacations);
    header('Location: vacations.php');
    exit;
}

// Approuver/Rejeter un congé
if (isset($_GET['action']) && isset($_GET['id'])) {
    $id = $_GET['id'];
    $action = $_GET['action'];
    foreach ($vacations as &$vacation) {
        if ($vacation['id'] == $id) {
            $vacation['status'] = $action;
            break;
        }
    }
    save_vacations($vacations);
    header('Location: vacations.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demandes de Congé - HIY</title>
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
            <h2>Demander un Congé</h2>
            <form method="post">
                <label for="employee_id">Employé:</label>
                <select id="employee_id" name="employee_id" required>
                    <?php foreach ($employees as $employee): ?>
                    <option value="<?php echo $employee['id']; ?>"><?php echo $employee['name']; ?></option>
                    <?php endforeach; ?>
                </select>
                <label for="start_date">Date de Début:</label>
                <input type="date" id="start_date" name="start_date" required>
                <label for="end_date">Date de Fin:</label>
                <input type="date" id="end_date" name="end_date" required>
                <label for="reason">Raison:</label>
                <textarea id="reason" name="reason"></textarea>
                <button type="submit" name="request_vacation">Demander Congé</button>
            </form>
        </section>
        <section>
            <h2>Demandes de Congé</h2>
            <table>
                <thead>
                    <tr>
                        <th>Employé</th>
                        <th>Date Début</th>
                        <th>Date Fin</th>
                        <th>Raison</th>
                        <th>Statut</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($vacations as $vacation): ?>
                    <tr>
                        <td><?php echo $employees[array_search($vacation['employee_id'], array_column($employees, 'id'))]['name']; ?></td>
                        <td><?php echo $vacation['start_date']; ?></td>
                        <td><?php echo $vacation['end_date']; ?></td>
                        <td><?php echo $vacation['reason']; ?></td>
                        <td><?php echo $vacation['status']; ?></td>
                        <td>
                            <?php if ($vacation['status'] == 'pending'): ?>
                            <a href="?action=approved&id=<?php echo $vacation['id']; ?>">Approuver</a> |
                            <a href="?action=rejected&id=<?php echo $vacation['id']; ?>">Rejeter</a>
                            <?php endif; ?>
                        </td>
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