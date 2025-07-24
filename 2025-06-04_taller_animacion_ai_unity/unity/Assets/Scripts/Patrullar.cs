using UnityEngine;
using UnityEngine.AI;

public class IAController : MonoBehaviour
{
    public Transform[] puntos;
    private int index = 0;

    public Transform jugador;

    private NavMeshAgent agent;
    private Animator animator;

    enum Estado { Patrullar, Perseguir }
    Estado estado = Estado.Patrullar;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
        animator = GetComponent<Animator>();

        if (puntos.Length > 0)
        {
            agent.SetDestination(puntos[0].position);
        }
    }

    void Update()
    {
        float distancia = Vector3.Distance(transform.position, jugador.position);

        if (distancia < 5f)
        {
            estado = Estado.Perseguir;
            agent.SetDestination(jugador.position);
        }
        else
        {
            estado = Estado.Patrullar;
        }

        if (estado == Estado.Patrullar)
        {
            if (!agent.pathPending && agent.remainingDistance < 0.5f)
            {
                index = (index + 1) % puntos.Length;
                agent.SetDestination(puntos[index].position);
            }
        }

        // Animación basada en movimiento
        float velocidad = agent.velocity.magnitude;
        animator.SetFloat("velocidad", velocidad);
    }

    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Player"))
        {
            animator.SetTrigger("alerta");
        }
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            animator.SetTrigger("alerta");
        }
    }

}
