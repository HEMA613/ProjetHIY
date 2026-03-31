<?php
include 'data.php';
$employees = load_employees();
$vacations = load_vacations();

// Filtrer les congés approuvés
$approved_vacations = array_filter($vacations, function($v) { return $v['status'] == 'approved'; });
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calendrier des Congés - HIY</title>
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
            <h2>Calendrier des Congés Approuvés</h2>
            <div id="calendar">
                <?php
                $current_month = date('m');
                $current_year = date('Y');
                $days_in_month = cal_days_in_month(CAL_GREGORIAN, $current_month, $current_year);
                ?>
                <h3><?php echo date('F Y'); ?></h3>
                <table>
                    <thead>
                        <tr>
                            <th>Lun</th>
                            <th>Mar</th>
                            <th>Mer</th>
                            <th>Jeu</th>
                            <th>Ven</th>
                            <th>Sam</th>
                            <th>Dim</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $first_day = date('N', strtotime("$current_year-$current_month-01"));
                        $day = 1;
                        for ($week = 0; $week < 6; $week++) {
                            echo '<tr>';
                            for ($weekday = 1; $weekday <= 7; $weekday++) {
                                if ($week == 0 && $weekday < $first_day) {
                                    echo '<td></td>';
                                } elseif ($day > $days_in_month) {
                                    echo '<td></td>';
                                } else {
                                    $date = sprintf('%04d-%02d-%02d', $current_year, $current_month, $day);
                                    $vacation_employees = [];
                                    foreach ($approved_vacations as $vacation) {
                                        if ($date >= $vacation['start_date'] && $date <= $vacation['end_date']) {
                                            $employee_name = $employees[array_search($vacation['employee_id'], array_column($employees, 'id'))]['name'];
                                            $vacation_employees[] = $employee_name;
                                        }
                                    }
                                    echo '<td>';
                                    echo $day;
                                    if (!empty($vacation_employees)) {
                                        echo '<br><small>' . implode(', ', $vacation_employees) . '</small>';
                                    }
                                    echo '</td>';
                                    $day++;
                                }
                            }
                            echo '</tr>';
                            if ($day > $days_in_month) break;
                        }
                        ?>
                    </tbody>
                </table>
            </div>
        </section>
    </main>
    <footer>
        <p>&copy; 2024 HIY - Système de Gestion des Congés</p>
    </footer>
</body>
</html>