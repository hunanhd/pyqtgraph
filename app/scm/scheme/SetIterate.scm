;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;����             ;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define SetIterate
 (lambda()
   ;; �����ٶ�ѹ����Ϸ���Ϊsimplec
   ;(ti-menu-load-string "/solve/set/p-v-coupling 21")
   ;(ti-menu-load-string "/solve/set/p-v-controls 1")


    ;;����ch4�ɳ�����
;   (ti-menu-load-string "/solve/set/under-relaxation/species-0 0.8")
; ;;����o2�ɳ�����
;   (ti-menu-load-string "/solve/set/under-relaxation/species-1 0.8")
; ;;;;����co2�ɳ�����
;   (ti-menu-load-string "/solve/set/under-relaxation/species-2 0.8")
; ;;;;;����co�ɳ�����
;   (ti-menu-load-string "/solve/set/under-relaxation/species-3 0.8")
; ;;;;;����h2o�ɳ�����
;   (ti-menu-load-string "/solve/set/under-relaxation/species-4 0.8")
; ;;;;;����energy�ɳ�����
;   (ti-menu-load-string "/solve/set/under-relaxation/temperature 0.8")
 
   (ti-menu-load-string "/solve/iterate 200")                   ;;���������õ�������10000
 )
)
(SetIterate)
