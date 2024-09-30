package com.example.intellihome

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatButton
import androidx.core.view.ViewCompat
import android.widget.EditText
import android.widget.Toast
import androidx.core.view.WindowInsetsCompat
import java.io.PrintWriter
import java.net.Socket
import java.util.Scanner
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {
    private var socket: Socket? = null
    private var out: PrintWriter? = null
    private var `in`: Scanner? = null
    private val handler = Handler(Looper.getMainLooper()) // Para actualizar la UI desde el hilo de recepción

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val paso1login = findViewById<EditText>(R.id.edit1)
        val paso2login = findViewById<EditText>(R.id.edit2)
        val botonmenu = findViewById<AppCompatButton>(R.id.btnmenu)

        botonmenu.setOnClickListener {
            val usuarioocoreo = paso1login.text.toString()
            val contraseña = paso2login.text.toString()
            if (usuarioocoreo.isEmpty() || contraseña.isEmpty()) {
                Toast.makeText(this, "Por favor, completa ambos campos.", Toast.LENGTH_SHORT).show()
            } else {
                sendMessage("$usuarioocoreo,$contraseña") // Enviar mensaje
                println("Yo: $usuarioocoreo,$contraseña")
            }
        }

        // Configuración del botón para ir al registro
        val botonregistro = findViewById<AppCompatButton>(R.id.botregistro)
        botonregistro.setOnClickListener {
            val lanzar = Intent(this, MainActivity2::class.java)
            startActivity(lanzar)
        }

        // Iniciar conexión al servidor en un hilo separado
        thread {
            try {
                println("Intentando conectar al servidor...")
                socket = Socket("10.0.2.2", 2020)
                println("Conectado")
                out = PrintWriter(socket?.getOutputStream(), true)
                `in` = Scanner(socket?.getInputStream())

                // Hilo para recibir respuestas del servidor
                while (true) {
                    if (`in`?.hasNextLine() == true) {
                        val response = `in`?.nextLine() // Leer respuesta del servidor
                        println("Servidor: $response")

                        // Publicar el resultado en el hilo principal
                        handler.post {
                            handleServerResponse(response)
                        }
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // Función para enviar mensaje al servidor
    private fun sendMessage(message: String) {
        thread {
            try {
                out?.println(message)
                out?.flush() // Asegurarse de que el mensaje se envíe inmediatamente
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // Manejar la respuesta del servidor
    private fun handleServerResponse(response: String?) {
        println("Response: $response")
        if (response == "true") {
            val menu = Intent(this, MainActivity3::class.java)
            startActivity(menu)
        } else {
            println("Fallo34")
            Toast.makeText(this, "Autenticación fallida", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            out?.close()
            `in`?.close()
            socket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
