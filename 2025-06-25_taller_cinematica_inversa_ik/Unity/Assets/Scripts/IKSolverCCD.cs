using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IKSolverCCD : MonoBehaviour
{
    [Header("Configuraci�n del brazo")]
    public Transform[] joints;     // Lista de articulaciones desde la mano hasta la base
    public Transform target;       // Objetivo que debe alcanzar
    public int maxIterations = 10; // Iteraciones por frame (m�ximo de giros)
    public float threshold = 0.01f; // Distancia m�nima al objetivo para detener

    void Update()
    {
        SolveIK();

        // Visualiza una l�nea entre la mano y el objetivo
        Debug.DrawLine(joints[0].position, target.position, Color.red);
    }

    void SolveIK()
    {
        if (joints == null || joints.Length == 0 || target == null) return;

        // Iterar varias veces por frame para mejorar precisi�n
        for (int i = 0; i < maxIterations; i++)
        {
            // Recorre todas las articulaciones desde la mano hacia la base
            for (int j = 0; j < joints.Length - 1; j++)
            {
                Transform joint = joints[j];

                // Vector desde articulaci�n a la mano (extremo)
                Vector3 toEnd = joints[0].position - joint.position;

                // Vector desde articulaci�n al objetivo
                Vector3 toTarget = target.position - joint.position;

                // Calcula �ngulo de rotaci�n entre vectores
                float angle = Vector3.SignedAngle(toEnd, toTarget, Vector3.forward);

                // Rota la articulaci�n (en el eje Z si es 2D)
                joint.Rotate(Vector3.forward, angle);

                // Detiene si la distancia al objetivo es suficientemente peque�a
                if ((joints[0].position - target.position).magnitude < threshold)
                    return;
            }
        }
    }
}


