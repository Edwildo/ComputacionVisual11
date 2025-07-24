using UnityEngine;

[RequireComponent(typeof(CharacterController))]
public class PlayerMovement : MonoBehaviour
{
    public float speed = 5f;
    public float gravity = -9.81f;

    private CharacterController controller;
    private Vector3 velocity;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        float horizontal = Input.GetAxis("Horizontal"); // A/D
        float vertical = Input.GetAxis("Vertical");     // W/S

        Vector3 move = new Vector3(horizontal, 0f, vertical).normalized;
        controller.Move(move * speed * Time.deltaTime);

        // Gravedad (mantener al jugador en el suelo)
        if (!controller.isGrounded)
        {
            velocity.y += gravity * Time.deltaTime;
            controller.Move(velocity * Time.deltaTime);
        }
        else
        {
            velocity.y = -2f;
        }

        // 🔒 Bloqueamos rotación manualmente en caso de que algo la afecte
        transform.rotation = Quaternion.identity;
    }
}
