;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;计算             ;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define SetIterate
 (lambda()
   ;; 设置速度压力耦合方法为simplec
   ;(ti-menu-load-string "/solve/set/p-v-coupling 21")
   ;(ti-menu-load-string "/solve/set/p-v-controls 1")


    ;;设置ch4松弛因子
;   (ti-menu-load-string "/solve/set/under-relaxation/species-0 0.8")
; ;;设置o2松弛因子
;   (ti-menu-load-string "/solve/set/under-relaxation/species-1 0.8")
; ;;;;设置co2松弛因子
;   (ti-menu-load-string "/solve/set/under-relaxation/species-2 0.8")
; ;;;;;设置co松弛因子
;   (ti-menu-load-string "/solve/set/under-relaxation/species-3 0.8")
; ;;;;;设置h2o松弛因子
;   (ti-menu-load-string "/solve/set/under-relaxation/species-4 0.8")
; ;;;;;设置energy松弛因子
;   (ti-menu-load-string "/solve/set/under-relaxation/temperature 0.8")
 
   (ti-menu-load-string "/solve/iterate 200")                   ;;迭代，设置迭代次数10000
 )
)
(SetIterate)
