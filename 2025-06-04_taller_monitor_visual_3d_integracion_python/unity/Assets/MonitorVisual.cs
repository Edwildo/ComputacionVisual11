using UnityEngine;
using System.IO;
using System.Diagnostics;
using System;

public class MonitorVisual : MonoBehaviour
{
    public GameObject sphere1, sphere2;
    public GameObject fingerObject1, fingerObject2;

    private string jsonPath;
    private Process pythonProcess;

    [System.Serializable]
    public class VisualData
    {
        public int person_count;
        public int finger_count;
        public int frame_width;
        public int frame_height;
    }

    void Start()
    {
        // Ruta al JSON
        jsonPath = Path.Combine(Application.dataPath, "person_data.json");

        // Obtener ruta relativa al script Python (sube desde /Assets/ a raíz del proyecto)
        string basePath = Directory.GetParent(Application.dataPath).FullName;
        string scriptPath = Path.Combine(basePath, "../python/generar_json.py");

        // Ejecutar Python
        string pythonExe = "python"; // Cambia a "python3" si usas Mac/Linux

        try
        {
            pythonProcess = new Process();
            pythonProcess.StartInfo.FileName = pythonExe;
            pythonProcess.StartInfo.Arguments = $"\"{scriptPath}\"";
            pythonProcess.StartInfo.UseShellExecute = false;
            pythonProcess.StartInfo.CreateNoWindow = true;
            pythonProcess.Start();
            UnityEngine.Debug.Log("🟢 Python iniciado desde ruta relativa.");
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("❌ Error al iniciar Python: " + ex.Message);
        }
    }

    void Update()
    {
        if (File.Exists(jsonPath))
        {
            try
            {
                using (FileStream stream = new FileStream(jsonPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                using (StreamReader reader = new StreamReader(stream))
                {
                    string json = reader.ReadToEnd();
                    VisualData data = JsonUtility.FromJson<VisualData>(json);

                    if (data != null)
                    {
                        // 🎨 Colores según número de personas
                        Color color = Color.white;
                        if (data.person_count == 1) color = Color.green;
                        else if (data.person_count == 2) color = Color.red;
                        else if (data.person_count >= 3) color = Color.yellow;

                        sphere1.GetComponent<Renderer>().material.color = color;
                        sphere2.GetComponent<Renderer>().material.color = color;

                        // 📏 Escala según número de dedos
                        float scaleFactor = 1f + data.finger_count * 0.8f;
                        fingerObject1.transform.localScale = Vector3.one * scaleFactor;
                        fingerObject2.transform.localScale = Vector3.one * scaleFactor;
                    }
                }
            }
            catch (IOException e)
            {
                UnityEngine.Debug.LogWarning("⚠️ Archivo ocupado, se reintentará: " + e.Message);
            }
        }
    }

    void OnApplicationQuit()
    {
        if (pythonProcess != null && !pythonProcess.HasExited)
        {
            pythonProcess.Kill();
            UnityEngine.Debug.Log("🔴 Python detenido al cerrar la aplicación.");
        }
    }
}
