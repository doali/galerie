(defun my/clean-url-and-spaces ()
  "Remplace tous les '%20' par des espaces et supprime 'http://galerie:8000/'."
  (interactive)
  (let ((start (if (use-region-p) (region-beginning) (point-min)))
        (end (if (use-region-p) (region-end) (point-max))))
    (save-excursion
      (save-restriction
        (narrow-to-region start end)

        ;; 1. s/http:\/\/galerie:8000\///g
        (goto-char (point-min))
        (while (search-forward "http://galerie:8000/" nil t)
          (replace-match ""))

        ;; 2. s/%20/\ /g
        (goto-char (point-min))
        (while (search-forward "%20" nil t)
          (replace-match " "))))))
