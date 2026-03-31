<?php
include 'data.php';
$employees = load_employees();
$vacations = load_vacations();
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestion des Congés - HIY</title>
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
        <section id="dashboard">
            <h2>Tableau de Bord</h2>
            <div class="stats">
                <div class="stat">
                    <h3>Nombre d'Employés</h3>
                    <p><?php echo count($employees); ?></p>
                </div>
                <div class="stat">
                    <h3>Demandes en Attente</h3>
                    <p><?php echo count(array_filter($vacations, function($v) { return $v['status'] == 'pending'; })); ?></p>
                </div>
                <div class="stat">
                    <h3>Congés Approuvés</h3>
                    <p><?php echo count(array_filter($vacations, function($v) { return $v['status'] == 'approved'; })); ?></p>
                </div>
            </div>
        </section>
    </main>
    <footer>
        <p>&copy; 2026 HIY - Système de Gestion des Congés</p>
    </footer>
</body>
</html>