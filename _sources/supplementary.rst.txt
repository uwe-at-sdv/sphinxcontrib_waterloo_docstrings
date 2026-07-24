Supplementary tests
===================

In this chapter we test the following:

* Method documentation boxes as referentiable objects
* Constants in module documentation boxes as referentiable objects
* Constants in classes inside classes as referentiable objects
* Variables in classes as referentiable objects
* Classes inside the modul as referentiable objects

.. wtrl_autodoc_module:: doc_method_resolution

.. wtrl_push_current_module:: doc_method_resolution

.. wtrl_autodoc_class_full:: X

.. wtrl_autodoc_class_full:: Y

.. wtrl_autodoc_class:: Y.INSIDE_Y

.. wtrl_pop_current_module:: doc_method_resolution

.. wtrl_autodoc_class:: doc_method_resolution.A

.. wtrl_autodoc_method:: doc_method_resolution.A.m

.. wtrl_autodoc_class:: doc_method_resolution.A.INSIDE_A

.. wtrl_autodoc_class:: doc_method_resolution.B

.. wtrl_autodoc_method:: doc_method_resolution.B.m

