using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CameraSwitcher : MonoBehaviour
{
    [Header("Referencias de la escena")]
    public Camera cam;                  
    public TMP_Text modeText;           
    public Slider orthoSlider;          

    void Awake()
    {
        // Revisar referencias antes de nada
        if (cam == null || modeText == null || orthoSlider == null)
        {
            Debug.LogError("CameraSwitcher: faltan referencias (Camera, Text o Slider).");
            enabled = false;
            return;
        }
    }

    void Start()
    {
        // 1) Configurar rango y valor inicial del slider
        orthoSlider.minValue = 2;
        orthoSlider.maxValue = 10;
        orthoSlider.value = cam.orthographicSize = 5;

        // 2) Suscribir el listener desde el código
        orthoSlider.onValueChanged.AddListener(AdjustOrthoSize);

        // 3) Actualizar UI para mostrar el estado inicial
        UpdateUI();
    }

    // Alterna entre Perspective y Orthographic
    public void ToggleProjection()
    {
        cam.orthographic = !cam.orthographic;

        // Si pasamos a ortográfica, fijar el tamaño actual del slider
        if (cam.orthographic)
            cam.orthographicSize = orthoSlider.value;

        UpdateUI();
    }

    // Ajusta el tamaño de la cámara ortográfica (invocado por el slider)
    public void AdjustOrthoSize(float size)
    {
        if (cam.orthographic)
            cam.orthographicSize = Mathf.Clamp(size, orthoSlider.minValue, orthoSlider.maxValue);
    }

    // Refresca el texto y visibilidad del slider
    void UpdateUI()
    {
        modeText.text = "Current: " + (cam.orthographic ? "Orthographic" : "Perspective");
        orthoSlider.gameObject.SetActive(cam.orthographic);
    }

    void Update()
    {
        // P para imprimir la matriz de proyección
        if (Input.GetKeyDown(KeyCode.P))
            Debug.Log("Projection Matrix:\n" + cam.projectionMatrix);
    }
}
