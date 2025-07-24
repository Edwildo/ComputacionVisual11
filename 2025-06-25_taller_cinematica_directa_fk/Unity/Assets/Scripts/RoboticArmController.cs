using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RoboticArmController : MonoBehaviour
{
    [Header("Partes del Brazo")]
    public Transform baseJoint;    // Rota en el eje Y
    public Transform arm1Joint;    // Rota en el eje X
    public Transform arm2Joint;    // Rota en el eje X
    public Transform clawTip;      // Usado para línea de depuración + marcador

    [Header("Controles UI")]
    public Slider baseSlider;
    public Slider arm1Slider;
    public Slider arm2Slider;
    public Toggle autoToggle;

    [Header("Configuración de Movimiento")]
    public float autoSpeed = 1.5f;       // Velocidad de la onda senoidal
    public float autoAmplitude = 45f;    // Amplitud máxima en grados

    private void Update()
    {
        if (autoToggle.isOn)
        {
            AplicarMovimientoAutomatico();
        }
        else
        {
            AplicarRotacionManual();
        }

        DibujarLineasDebug();
    }

    void AplicarRotacionManual()
    {
        baseJoint.localRotation = Quaternion.Euler(0f, baseSlider.value, 0f);
        arm1Joint.localRotation = Quaternion.Euler(arm1Slider.value, 0f, 0f);
        arm2Joint.localRotation = Quaternion.Euler(arm2Slider.value, 0f, 0f);
    }

    void AplicarMovimientoAutomatico()
    {
        float valorSin = Mathf.Sin(Time.time * autoSpeed);

        baseJoint.localRotation = Quaternion.Euler(0f, valorSin * autoAmplitude, 0f);
        arm1Joint.localRotation = Quaternion.Euler(valorSin * autoAmplitude, 0f, 0f);
        arm2Joint.localRotation = Quaternion.Euler(valorSin * autoAmplitude * 0.5f, 0f, 0f);
    }

    void DibujarLineasDebug()
    {
        Debug.DrawLine(baseJoint.position, arm1Joint.position, Color.red);
        Debug.DrawLine(arm1Joint.position, arm2Joint.position, Color.green);
        Debug.DrawLine(arm2Joint.position, clawTip.position, Color.blue);
    }
}
