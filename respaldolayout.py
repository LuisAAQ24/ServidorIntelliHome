<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/main"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity2">

    <ScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        tools:layout_editor_absoluteX="0dp"
        tools:layout_editor_absoluteY="70dp">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp">

            <TextView
                android:id="@+id/textView3"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Crear tu cuenta"
                android:textColor="@color/black"
                android:textSize="24sp"
                android:textStyle="bold"
                android:layout_marginBottom="10dp"
                android:layout_gravity="center"/>


            <TextView
                android:id="@+id/textView2"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginBottom="10dp"
                android:layout_gravity="center"
                android:text="Agrega una foto de perfil"
                android:textColor="@color/black"
                android:textStyle="bold"/>

            <ImageButton
                android:id="@+id/imageButton"
                android:layout_width="130dp"
                android:layout_height="130dp"
                tools:srcCompat="@tools:sample/avatars"
                android:layout_gravity="center"/>

            <EditText
                android:id="@+id/editnombre"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginBottom="10dp"
                android:layout_marginTop="30dp"
                android:hint="Ingrese su nombre"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>

            <EditText
                android:id="@+id/editapellido"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:hint="Ingrese sus apellidos"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>

            <EditText
                android:id="@+id/editnickname"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:hint="Ingrese un Nickname"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>

            <EditText
                android:id="@+id/textView6"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:hint="Mensaje1"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>


            <EditText
                android:id="@+id/textView8"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:hint="Mensaje1"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>

            <EditText
                android:id="@+id/textView9"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginBottom="10dp"
                android:hint="Mensaje1"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>
            <EditText
                android:id="@+id/textView10"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_marginBottom="10dp"
                android:hint="Mensaje1"
                android:textColorHint="#808080"
                android:layout_gravity="center"/>
            <Button
                android:id="@+id/button"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Botón al final"
                app:layout_constraintBottom_toBottomOf="parent"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintHorizontal_bias="0.497"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintTop_toTopOf="@+id/textView3"
                android:layout_marginBottom="100dp"
                app:layout_constraintVertical_bias="1.0" />

        </LinearLayout>
    </ScrollView>


</androidx.constraintlayout.widget.ConstraintLayout>