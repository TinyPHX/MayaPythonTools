/****************************************************************************
**
** Copyright (C) 2012 Digia Plc and/or its subsidiary(-ies).
** Contact: http://www.qt-project.org/legal
**
** This file is part of the demonstration applications of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Licensees holding valid Qt Commercial licenses may use this file in
** accordance with the Qt Commercial License Agreement provided with the 
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and Digia.  
**
** If you have questions regarding the use of this file, please use
** contact form at http://qt.digia.com
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick 1.0

Item {
    id: main
    //height and width set by program to fill window
    //below properties are sometimes set from C++
    property url qmlFile: ''
    property bool show: false

    Item{ id:embeddedViewer
        width: parent.width
        height: parent.height
        opacity: 0;
        z: 10
        Loader{
            id: loader
            z: 10
            focus: true //Automatic FocusScope
            clip: true
            source: qmlFile
            anchors.centerIn: parent
            onStatusChanged:{
            if(status == Loader.Null) {
                loader.focus = false;//fixes QTBUG11411, probably because the focusScope needs to gain focus to focus the right child
            }else if(status == Loader.Ready) {
                if(loader.item.width > 640)
                    loader.item.width = 640;
                if(loader.item.height > 480)
                    loader.item.height = 480;
            }}

        }
        Rectangle{ id: frame
            z: 9
            anchors.fill: loader.status == Loader.Ready ? loader : errorTxt
            anchors.margins: -8
            radius: 4
            smooth: true
            border.color: "#88aaaaaa"
            gradient: Gradient{
                GradientStop{ position: 0.0; color: "#14FFFFFF" }
                GradientStop{ position: 1.0; color: "#5AFFFFFF" }
            }
            MouseArea{
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
                onClicked: loader.focus=true;/* and don't propagate to the 'exit' area*/
            }

            Rectangle{ id: innerFrame
                anchors.margins: 7
                anchors.bottomMargin: 8
                anchors.rightMargin: 8
                color: "black"
                border.color: "#44000000"
                anchors.fill:parent
            }

        }
        Rectangle{ id: closeButton
            width: 24
            height: 24
            z: 11
            border.color: "#aaaaaaaa"
            gradient: Gradient{
                GradientStop{ position: 0.0; color: "#34FFFFFF" }
                GradientStop{ position: 1.0; color: "#7AFFFFFF" }
            }
            anchors.left: frame.right
            anchors.bottom: frame.top
            anchors.margins: -(2*width/3)
            Text{
                text: 'X'
                font.bold: true
                color: "white"
                font.pixelSize: 12
                anchors.centerIn: parent
            }
            MouseArea{
                anchors.fill: parent
                onClicked: main.show = false;
            }
        }

        Text{
            id: errorTxt
            z: 10
            anchors.centerIn: parent
            color: 'white'
            smooth: true
            visible: loader.status == Loader.Error
            textFormat: Text.RichText
            //Note that if loader is Error, it is because the file was found but there was an error creating the component
            //This means either we have a bug in our demos, or the required modules (which ship with Qt) did not deploy correctly
            text: "The example has failed to load.<br />If you installed all Qt's C++ and QML modules then this is a bug!<br />"
                + 'Report it at <a href="http://bugreports.qt-project.org">http://bugreports.qt-project.org</a>';
            onLinkActivated: Qt.openUrlExternally(link);
        }
    }
    Rectangle{ id: blackout //Maybe use a colorize effect instead?
        z: 8
        anchors.fill: parent
        color: "#000000"
        opacity: 0
    }
    MouseArea{
        z: 8
        enabled: main.show
        hoverEnabled: main.show //To steal focus from the buttons
        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
        anchors.fill: parent
    }

    states: [
        State {
            name: "show"
            when: show == true
            PropertyChanges {
                target: embeddedViewer
                opacity: 1
            }
            PropertyChanges {
                target: blackout
                opacity: 0.5
            }
        }
    ]
    transitions: [//Should not be too long, because the component has already started running
        Transition { from: ''; to: "show"; reversible: true
            ParallelAnimation{
                NumberAnimation{ properties: "opacity"; easing.type: Easing.InQuad; duration: 500}
                PropertyAction { target: loader; property: "focus"; value: true}//Might be needed to ensure the focus stays with us
            }
        }
    ]
}
