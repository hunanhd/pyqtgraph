;湍流方程
(ti-menu-load-string "/define/models/viscous/ke-standard? y") 
;设置边界条件
(ti-menu-load-string "/define/boundary-conditions/velocity-inlet inlet n n y y  n  6.87 y n 1 n 1") 
;设置收敛标准参数
(ti-menu-load-string "/solve/monitors/residual/convergence-criteria 0.0001 0.0001 0.0001 0.0001 0.0001") 
;设置迭代式的动态
(ti-menu-load-string "/solve/monitors/residual/plot? y") 
