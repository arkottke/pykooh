#include <math.h>
#include "smoothing.h"

/*
 * This code implements Konno-Ohmachi spectral smoothing as defined in their
 * paper:
 * Konno, K. and Ohmachi, T., 1998. Ground-motion characteristics estimated
 * from spectral ratio between horizontal and vertical components of
 * microtremor. Bulletin of the Seismological Society of America, 88(1),
 * pp.228-241.
 * The function below is partially based on a Python version by Albert
 * Kottke and found here:
 * https://github.com/arkottke/notebooks/blob/master/effective_amp_spectrum.ipynb
 * It was rewritten and optimized in C by Bruce Worden.
 */
void konno_ohmachi_c(
        double *spec,
        double *freqs,
        int ns,
        double *ko_freqs,
        double *ko_smooth,
        int nks,
        double b) {
    int i, j;
    double window_total, total, x, fc, freq, frat, window;
    double max_ratio = pow(10.0, (3.0 / b));
    double min_ratio = 1.0 / max_ratio;

    for(i = 0; i < nks; i++) {
        fc = ko_freqs[i];
        if (fc < 1e-6) {
            ko_smooth[i] = 0;
            continue;
        }
        total = 0;
        window_total = 0;
        for(j = 0; j < ns; j++) {
            freq = freqs[j];
            frat = freq / fc;
            if (freq < 1e-6 ||
                frat > max_ratio || frat < min_ratio) {
                continue;
            } else if (fabs(freq - fc) < 1e-6) {
                window = 1.0;
            } else {
                x = b * log10(frat);
                window = sin(x) / x;
                window *= window;
                window *= window;
            }
            total += window * spec[j];
            window_total += window;
        }
        if (window_total > 0) {
            ko_smooth[i] = total / window_total;
        } else {
            ko_smooth[i] = 0;
        }
    }
    return;
}
