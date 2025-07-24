using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class MoverObjetivo : MonoBehaviour
{
    public Transform objetivo;     // La esfera
    public Slider sliderX, sliderY, sliderZ;

    void Update()
    {
        if (objetivo != null)
        {
            objetivo.position = new Vector3(
                sliderX.value,
                sliderY.value,
                sliderZ.value
            );
        }
    }
}
