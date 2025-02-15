# CS421 Project 1
## Automated Eye Tracking Data Correction
### *Ben Raivel*

## Abstract:
In this project I replicated part of the paper: *Carr, Jon W., et al. "Algorithms for the automated correction of vertical drift in eye-tracking data." Behavior Research Methods 54.1 (2022): 287-310.* Using the replication package, I compared the performance of ten algorithms on five types of error: gaussian noise, slope distortion, shift distortion, within-line regression, and between-line regression.

## Results:
### Gaussian Noise:
![Noise Plot](noise_comparison.png)

| Algorithm | Accuracy |
|-----------|----------|
| split | 0.97 |
| chain | 0.96 |
| warp | 0.93 |
| attach | 0.91 |
| regress | 0.89 |
| stretch | 0.88 |
| cluster | 0.88 |
| compare | 0.86 |
| merge | 0.86 |
| segment | 0.80 |

### Slope Distortion:
![Slope Distortion Plot](slope_dist_accuracy.png)

| Algorithm | Accuracy |
|-----------|----------|
| merge | 0.97 |
| warp | 0.91 |
| regress | 0.90 |
| compare | 0.87 |
| cluster | 0.80 |
| segment | 0.80 |
| stretch | 0.76 |
| attach | 0.69 |
| chain | 0.67 |
| split | 0.64 |

### Shift Distortion:
![Shift Distortion Plot](shift_dist_accuracy.png)

| Algorithm | Accuracy |
|-----------|----------|
| cluster | 1.0 |
| merge | 0.99 |
| regress | 0.98 |
| warp | 0.92 |
| stretch | 0.91 |
| chain | 0.89 |
| attach | 0.88 |
| split | 0.87 |
| compare | 0.86 |
| segment | 0.80 |

### Within Line Regression:
![Within Line Plot](within_line_accuracy.png)

| Algorithm | Accuracy |
|-----------|----------|
| attach | 0.46 |
| chain | 0.46 |
| cluster | 0.46 |
| regress | 0.46 |
| stretch | 0.46 |
| merge | 0.45 |
| split | 0.45 |
| warp | 0.43 |
| compare | 0.39 |
| segment | 0.38 |

### Between Line Regression:
![Between Line Plot](between_line_accuracy.png)

| Algorithm | Accuracy |
|-----------|----------|
| attach | 0.49 |
| chain | 0.49 |
| cluster | 0.49 |
| regress | 0.49 |
| stretch | 0.49 |
| merge | 0.48 |
| split | 0.47 |
| warp | 0.46 |
| compare | 0.42 |
| segment | 0.40|

## Discussion:
The performance on gaussian noise is similar to Figure 4a in the paper: regress, stretch, cluster, and merge have similar performance— accuracy decreases most quickly for these algorithms; chain and attach are the next worst, accuracy declines but not as quickly; segment, compare, warp, and split perform the best, accuracy is constant as noise increases (the value accuracy is constant *at* is different from the paper).

The slope distortion plot closely resembles Figure 4b in the paper: split and chain perform the worst; regress exhibits strange behavior where accuracy declines then improves again as the distortion parameter increases; cluster, attach, and stretch have similar performance, though not as bad as split and chain; merge performs well at all distortions.

The shift distortion plot (Figure 4c) looks similar to mine with the exception of stretch, which has a similar profile to regress in my slope distortion plot, but does not exhibit that behavior in the data presented in the paper.

The accuracy plots for within-line and between-line regressions (Figures 4d and 4e in the paper) look much different from the ones I produced. In my plots all the algorithms perform roughly the same: accuracy drops rapidly at low rates of regression.