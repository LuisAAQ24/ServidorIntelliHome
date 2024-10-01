package com.example.intellihome

import android.Manifest
import android.app.DatePickerDialog
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*
import android.text.Editable
import android.text.TextWatcher

class MainActivity2 : AppCompatActivity() {
    private lateinit var editNombre: EditText
    private lateinit var editApellido: EditText
    private lateinit var editUsername: EditText
    private lateinit var editTelefono: EditText
    private lateinit var editHobbies: EditText
    private lateinit var editEmail: EditText
    private lateinit var editContrasena: EditText
    private lateinit var editConfirmarContrasena: EditText
    private lateinit var spinnerFormaPago: Spinner
    private lateinit var editNumeroTarjeta: EditText
    private lateinit var editFechaVencimiento: EditText
    private lateinit var editCVC: EditText
    private lateinit var textViewSeleccionFecha: TextView
    private lateinit var imageViewPerfil: ImageView
    private lateinit var buttonFechaNacimiento: Button
    private lateinit var buttonRegistrar: Button
    private lateinit var socketViewModel: SocketViewModel
    private var fechaNacimiento: String = ""

    private var selectedImageUri: Uri = Uri.EMPTY

    private val imagePickerLauncher = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        uri?.let {
            selectedImageUri = it
            imageViewPerfil.setImageURI(selectedImageUri)
        }
    }

    private val cameraLauncher = registerForActivityResult(ActivityResultContracts.TakePicture()) { success: Boolean ->
        if (success) {
            if (selectedImageUri != Uri.EMPTY) {
                imageViewPerfil.setImageURI(selectedImageUri)
            } else {
                Toast.makeText(this, "Error: URI de imagen no disponible", Toast.LENGTH_SHORT).show()
            }
        } else {
            Toast.makeText(this, "Error al capturar la imagen", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)

        editNombre = findViewById(R.id.editNombre)
        editApellido = findViewById(R.id.editApellido)
        editUsername = findViewById(R.id.editUsername)
        editTelefono = findViewById(R.id.editTelefono)
        editHobbies = findViewById(R.id.editHobbies)
        editEmail = findViewById(R.id.editEmail)
        editContrasena = findViewById(R.id.editContrasena)
        editConfirmarContrasena = findViewById(R.id.editConfirmarContrasena)
        spinnerFormaPago = findViewById(R.id.spinnerFormaPago)
        editNumeroTarjeta = findViewById(R.id.editNumeroTarjeta)
        editFechaVencimiento = findViewById(R.id.editFechaVencimiento)
        editCVC = findViewById(R.id.editCVC)
        textViewSeleccionFecha = findViewById(R.id.textViewSeleccionFecha)
        imageViewPerfil = findViewById(R.id.imageViewPerfil)
        buttonFechaNacimiento = findViewById(R.id.buttonFechaNacimiento)
        buttonRegistrar = findViewById(R.id.buttonRegistrar)

        buttonFechaNacimiento.setOnClickListener { mostrarFechaPicker() }
        buttonRegistrar.setOnClickListener { registrarUsuario() }

        imageViewPerfil.setOnClickListener { mostrarOpcionesDeImagen() }

        socketViewModel = ViewModelProvider(this).get(SocketViewModel::class.java)
        socketViewModel.connectToServer("10.0.2.2", 6060)

        val formasPago = arrayOf("Ambientalista", "Rustica", "Moderna", "Mansión")
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, formasPago)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        spinnerFormaPago.adapter = adapter

        // Agregar el TextWatcher al campo de fecha de vencimiento
        editFechaVencimiento.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                if (s != null && s.length == 2 && before < count) {
                    editFechaVencimiento.append("/")
                }
                if (s != null && s.length > 5) {
                    editFechaVencimiento.setText(s.subSequence(0, 5))
                    editFechaVencimiento.setSelection(5)
                }
            }

            override fun afterTextChanged(s: Editable?) {}
        })
    }

    private fun mostrarOpcionesDeImagen() {
        val opciones = arrayOf("Tomar foto", "Seleccionar de galería")
        AlertDialog.Builder(this)
            .setTitle("Seleccionar imagen")
            .setItems(opciones) { dialog, which ->
                when (which) {
                    0 -> {
                        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                            selectedImageUri = Uri.fromFile(createImageFile())
                            cameraLauncher.launch(selectedImageUri)
                        } else {
                            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), CAMERA_PERMISSION_CODE)
                        }
                    }
                    1 -> imagePickerLauncher.launch("image/*")
                }
            }
            .show()
    }

    private fun createImageFile(): File {
        val timeStamp: String = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val storageDir: File = getExternalFilesDir(Environment.DIRECTORY_PICTURES) ?: throw IOException("No se pudo acceder al directorio")
        return File.createTempFile("JPEG_${timeStamp}_", ".jpg", storageDir).apply {
            selectedImageUri = Uri.fromFile(this)
            Log.d("MainActivity2", "Archivo de imagen creado: $selectedImageUri")
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                mostrarOpcionesDeImagen()
            } else {
                Toast.makeText(this, "Permiso denegado para usar la cámara", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun mostrarFechaPicker() {
        val calendario = Calendar.getInstance()
        val year = calendario.get(Calendar.YEAR)
        val month = calendario.get(Calendar.MONTH)
        val day = calendario.get(Calendar.DAY_OF_MONTH)

        val datePicker = DatePickerDialog(this, { _, selectedYear, selectedMonth, selectedDay ->
            fechaNacimiento = "$selectedDay/${selectedMonth + 1}/$selectedYear"
            textViewSeleccionFecha.text = fechaNacimiento
        }, year, month, day)
        datePicker.show()
    }

    private fun registrarUsuario() {
        val nombre = editNombre.text.toString().trim()
        val apellido = editApellido.text.toString().trim()
        val username = editUsername.text.toString().trim()
        val telefono = editTelefono.text.toString().trim()
        val hobbies = editHobbies.text.toString().trim()
        val email = editEmail.text.toString().trim()
        val contrasena = editContrasena.text.toString().trim()
        val confirmarContrasena = editConfirmarContrasena.text.toString().trim()
        val formaPago = spinnerFormaPago.selectedItem.toString().trim()
        val numeroTarjeta = editNumeroTarjeta.text.toString().trim()
        val fechaVencimiento = editFechaVencimiento.text.toString().trim()
        val cvc = editCVC.text.toString().trim()

        if (nombre.isEmpty() || apellido.isEmpty() || username.isEmpty() || telefono.isEmpty() ||
            hobbies.isEmpty() || email.isEmpty() || contrasena.isEmpty() || confirmarContrasena.isEmpty() ||
            formaPago.isEmpty() || fechaVencimiento.isEmpty() || cvc.isEmpty() || fechaNacimiento.isEmpty() ||
            numeroTarjeta.isEmpty()) {
            Toast.makeText(this, "Por favor, completa todos los campos", Toast.LENGTH_SHORT).show()
            return
        }

        if (contrasena != confirmarContrasena) {
            Toast.makeText(this, "Las contraseñas no coinciden", Toast.LENGTH_SHORT).show()
            return
        }

        if (!isFechaValida(fechaVencimiento)) {
            Toast.makeText(this, "Formato de fecha vencimiento inválido. Debe ser MM/AA", Toast.LENGTH_SHORT).show()
            return
        }

        // Crear un string con los datos a enviar
        val usuarioData = "registro,$contrasena,$email,$username,$telefono,$apellido,$nombre,$nombre,$formaPago,$numeroTarjeta,$fechaVencimiento,$cvc,$fechaNacimiento,$hobbies"

        // Enviar los datos al servidor
        socketViewModel.sendMessage(usuarioData)

        // Mostrar un mensaje de éxito y volver a la actividad principal
        Toast.makeText(this, "Usuario registrado con éxito", Toast.LENGTH_SHORT).show()
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)
    }

    // Función para validar el formato MM/AA
    private fun isFechaValida(fecha: String): Boolean {
        val regex = Regex("\\d{2}/\\d{2}")
        return regex.matches(fecha)
    }

    companion object {
        private const val CAMERA_PERMISSION_CODE = 101
    }
}
