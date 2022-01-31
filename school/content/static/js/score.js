function calculPoints(countSecondes, secondes) {
    countSecondes = countSecondes - secondes;
        if (countSecondes <= 2) {
            points = 3;
        }
        if (countSecondes > 2 && countSecondes <=5) {
            points = 2;
        }
        if (countSecondes > 5 && countSecondes <=8) {
            points = 1;
        }
        if (countSecondes > 8) {
            points = 0;
        }
    return points;
}