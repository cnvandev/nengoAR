SPEED = 0.5;

desired_position = [1 2 1];
current_position = [0 0 0];

% MOTORS:
%
% 1    2
%  \  /
%   ++
%   ++
%  /  \
% 3    4

distance = desired_position - current_position;

motor1 = (distance(3) + distance(1) - distance(2)) * SPEED
motor2 = (distance(3) - distance(1) - distance(2)) * SPEED
motor3 = (distance(3) + distance(1) + distance(2)) * SPEED
motor4 = (distance(3) - distance(1) + distance(2)) * SPEED