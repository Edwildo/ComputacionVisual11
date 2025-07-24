using UnityEngine;

public class ObjectInterpolator : MonoBehaviour
{
    [Header("References")]
    public Transform pointA;
    public Transform pointB;
    public LineRenderer pathLine;
    public TMPro.TextMeshProUGUI progressText; // Opcional: Requiere TextMeshPro

    [Header("Settings")]
    [Range(0, 1)] public float t = 0f;
    public float duration = 3f;
    public bool autoMove = false;
    public AnimationCurve easeCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);

    private Quaternion startRotation;

    void Start()
    {
        // Configuraci�n inicial
        startRotation = transform.rotation;
        
        // Configurar l�nea de trayectoria
        if (pathLine != null)
        {
            pathLine.positionCount = 2;
            pathLine.SetPosition(0, pointA.position);
            pathLine.SetPosition(1, pointB.position);
        }
    }

    void Update()
    {
        // Control del tiempo (autom�tico o manual)
        if (autoMove)
        {
            t = Mathf.PingPong(Time.time / duration, 1f);
        }

        // Aplicar curva de easing
        float smoothedT = easeCurve.Evaluate(t);

        // Interpolaci�n de posici�n
        transform.position = Vector3.Lerp(pointA.position, pointB.position, smoothedT);

        // Interpolaci�n de rotaci�n
        Quaternion targetRotation = Quaternion.LookRotation(pointB.position - pointA.position);
        transform.rotation = Quaternion.Slerp(startRotation, targetRotation, smoothedT);

        // Actualizar UI (opcional)
        if (progressText != null)
        {
            progressText.text = $"Progress: {smoothedT * 100:F1}%";
        }

        // Dibujar debug line (visible en Scene View)
        Debug.DrawLine(pointA.position, pointB.position, Color.green);
    }

    // M�todo para reiniciar la animaci�n
    public void ResetAnimation()
    {
        t = 0f;
    }
}



