((python-mode . ((eval . (progn
                           (add-hook 'before-save-hook #'py-isort-before-save nil t)
                           (add-hook 'before-save-hook #'elpy-black-fix-code nil t))))))
