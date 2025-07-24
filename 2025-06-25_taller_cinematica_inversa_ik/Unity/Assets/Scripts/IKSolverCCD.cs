using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IKSolverCCD : MonoBehaviour
{
    [Header("Configuración del brazo")]
    public Transform[] joints;     // Lista de articulaciones desde la mano hasta la base
    public Transform target;       // Objetivo que debe alcanzar
    public int maxIterations = 10; // Iteraciones por frame (máximo de giros)
    public float threshold = 0.01f; // Distancia mínima al objetivo para detener

    void Update()
    {
        SolveIK();

        // Visualiza una línea entre la mano y el objetivo
        Debug.DrawLine(joints[0].position, target.position, Color.red);
    }

    void SolveIK()
    {
        if (joints == null || joints.Length == 0 || target == null) return;

        // Iterar varias veces por frame para mejorar precisión
        for (int i = 0; i < maxIterations; i++)
        {
            // Recorre todas las articulaciones desde la mano hacia la base
            for (int j = 0; j < joints.Length - 1; j++)
            {
                Transform joint = joints[j];

                // Vector desde articulación a la mano (extremo)
                Vector3 toEnd = joints[0].position - joint.position;

                // Vector desde articulación al objetivo
                Vector3 toTarget = target.position - joint.position;

                // Calcula ángulo de rotación entre vectores
                float angle = Vector3.SignedAngle(toEnd, toTarget, Vector3.forward);

                // Rota la articulación (en el eje Z si es 2D)
                joint.Rotate(Vector3.forward, angle);

                // Detiene si la distancia al objetivo es suficientemente pequeña
                if ((joints[0].position - target.position).magnitude < threshold)
                    return;
            }
        }
    }
}


