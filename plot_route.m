current = csvread('current.csv');
desired = csvread('desired.csv');
trajectory = csvread('trajectory.csv');
path = csvread('path.csv');
engines = csvread('engines.csv');

figure;
hold all;
plot3(current(:, 1), current(:, 2), current(:, 3));
plot3(desired(:, 1), desired(:, 2), desired(:, 3));
plot3(path(:, 1), path(:, 2), path(:, 3), 'rO');
plot3(trajectory(:, 1), trajectory(:, 2), trajectory(:, 3));
legend('Current Position', 'Desired Position', 'Actual Goal', 'Trajectory');
view(14, -14);

figure;
subplot(2, 1, 1);
plot(engines);
legend('Engine 1', 'Engine 2', 'Engine 3', 'Engine 4');
subplot(2, 1, 2);
plot(trajectory);
legend('x', 'y', 'z');