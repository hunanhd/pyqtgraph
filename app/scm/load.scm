;(system (string-append "del /s " "ffc_fluent.error"))

; (define port
;   (open-output-file "ffc_fluent.error")
;  )
; (close-output-port port)

(load '.\scheme\OpenCase.scm)
(load '.\scheme\setdefine.scm)
(load '.\scheme\Initialize.scm)

(load '.\scheme\SetIterate.scm)
(load '.\scheme\writedata.scm)
; (system (string-append "del /s " "ffc_fluent.error"))
;(exit)

(ti-menu-load-string "display/vector/velocity/velocity-magnitude")